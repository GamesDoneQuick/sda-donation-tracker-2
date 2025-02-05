import React, { useCallback, useEffect, useReducer } from 'react';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router';

import { useConstants } from '@common/Constants';
import { usePermission } from '@public/api/helpers/auth';
import useSafeDispatch from '@public/api/useDispatch';
import modelV2Actions from '@public/apiv2/actions/models';
import { Bid, findParent } from '@public/apiv2/Models';
import { useFetchParents } from '@public/hooks/useFetchParents';
import Spinner from '@public/spinner';

import styles from './donations.mod.css';

type Action = 'accept' | 'deny' | 'saving' | 'failed';

interface State {
  [k: number]: Action;
}

function stateReducer(state: State, { id, action }: { id: number; action: Action }) {
  return { ...state, [id]: action };
}

const stateMap = {
  accept: 'Accepted',
  deny: 'Denied',
  saving: 'Saving',
  failed: 'Failure while Saving',
};

export default React.memo(function ProcessPendingBids() {
  const { ADMIN_ROOT } = useConstants();
  const eventId = +useParams<{ eventId: string }>().eventId!;
  const status = useSelector((state: any) => state.status);
  const bids = useSelector((state: any) => state.models.bid) as Bid[];
  const event = useSelector((state: any) => state.models.event?.find((e: any) => e.pk === eventId));
  const canChangeBids = usePermission('tracker.change_bid');
  const canApproveBids = usePermission('tracker.approve_bid');
  const dispatch = useSafeDispatch();
  const fetchBids = useCallback(
    (e?: React.MouseEvent<HTMLButtonElement>) => {
      dispatch(modelV2Actions.loadBids({ feed: 'pending', eventId }));
      e?.preventDefault();
    },
    [dispatch, eventId],
  );
  const { loading } = useFetchParents();
  useEffect(() => {
    fetchBids();
  }, [fetchBids]);
  const [bidState, dispatchState] = useReducer(stateReducer, {} as State);
  const action = useCallback(
    ({ id, accept }: { id: number; accept: boolean }) => {
      dispatchState({ id, action: 'saving' });
      dispatch((accept ? modelV2Actions.approveBid : modelV2Actions.denyBid)(id))
        .then(() => {
          dispatchState({ id, action: accept ? 'accept' : 'deny' });
        })
        .catch(() => {
          dispatchState({ id, action: 'failed' });
        });
    },
    [dispatch],
  );

  return (
    <div>
      <h3>{event?.name}</h3>
      <button onClick={fetchBids}>Refresh</button>
      <Spinner spinning={status.bid === 'loading' || loading}>
        <table className="table table-condensed table-striped small">
          <thead>
            <tr>
              <th>Name</th>
              <th>Parent</th>
              {(canApproveBids || canChangeBids) && (
                <>
                  <th>Actions</th>
                  <th>Status</th>
                </>
              )}
            </tr>
          </thead>
          <tbody>
            {bids
              ?.filter(bid => bid.parent)
              .map(bid => {
                const parent = findParent(bids, bid);

                return (
                  <tr key={bid.id}>
                    <td>
                      <a href={`${ADMIN_ROOT}bid/${bid.id}`}>{bid.name}</a>
                    </td>
                    <td>
                      <a href={`${ADMIN_ROOT}bid/${bid.parent}`}>{parent?.name || '(unknown parent)'}</a>
                      {parent && parent.parent == null && parent.allowuseroptions && parent.option_max_length && (
                        <> &mdash; Max Option Length: {parent.option_max_length}</>
                      )}
                    </td>
                    {(canApproveBids || canChangeBids) && (
                      <>
                        <td>
                          <button
                            onClick={() =>
                              action({
                                id: bid.id,
                                accept: true,
                              })
                            }
                            disabled={bidState[bid.id] === 'saving'}>
                            Accept
                          </button>
                          <button
                            onClick={() =>
                              action({
                                id: bid.id,
                                accept: false,
                              })
                            }
                            disabled={bidState[bid.id] === 'saving'}>
                            Deny
                          </button>
                        </td>
                        <td className={styles['status']}>
                          <Spinner spinning={bidState[bid.id] === 'saving'}>
                            {bidState[bid.id] && stateMap[bidState[bid.id]]}
                          </Spinner>
                        </td>
                      </>
                    )}
                  </tr>
                );
              })}
          </tbody>
        </table>
      </Spinner>
    </div>
  );
});
