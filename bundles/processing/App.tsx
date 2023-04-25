import * as React from 'react';
import { Route, Switch } from 'react-router';
import { Accent, AppContainer, Theme } from '@spyrothon/sparx';

import { useConstants } from '@common/Constants';
import { usePermission } from '@public/api/helpers/auth';
import { setAPIRoot } from '@public/apiv2/HTTPUtils';
import { ProcessingSocket } from '@public/apiv2/sockets/ProcessingSocket';

import { loadDonations } from './modules/donations/DonationsStore';
import { setEventTotalIfNewer } from './modules/event/EventTotalStore';
import useProcessingStore from './modules/processing/ProcessingStore';
import * as Theming from './modules/theming/Theming';
import ProcessDonations from './pages/ProcessDonations';
import ReadDonations from './pages/ReadDonations';

import '../.design_system/generated/DesignSystem.css';
import '@spyrothon/sparx/style.css';

export default function App() {
  const canChangeDonations = usePermission('tracker.change_donation');
  const { processDonation } = useProcessingStore();
  const { theme, accent } = Theming.useThemeStore();

  const { APIV2_ROOT } = useConstants();

  React.useEffect(() => {
    setAPIRoot(APIV2_ROOT);
  }, [APIV2_ROOT]);

  React.useEffect(() => {
    const unsubActions = ProcessingSocket.on('processing_action', event => {
      loadDonations([event.donation]);
      if (event.action !== 'unprocessed') {
        processDonation(event.donation, event.action, false);
      }
    });

    const unsubNewDonations = ProcessingSocket.on('donation_received', event => {
      loadDonations([event.donation]);
      setEventTotalIfNewer(event.event_total, event.donation_count, new Date(event.posted_at).getTime());
    });

    return () => {
      unsubActions();
      unsubNewDonations();
    };
  }, [processDonation]);

  return (
    <AppContainer theme={theme as Theme} accent={accent as Accent}>
      <Switch>
        {canChangeDonations && (
          <>
            <Route path="/v2/:eventId/processing/donations" exact component={ProcessDonations} />
            <Route path="/v2/:eventId/processing/read" exact component={ReadDonations} />
          </>
        )}
      </Switch>
    </AppContainer>
  );
}
