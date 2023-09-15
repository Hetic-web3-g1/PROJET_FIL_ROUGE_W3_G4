import { Types } from '../actions/type';

const initialState = {
  filters: {
    sort_by: 'Created at',
    sort_by_status: [['Completed', false], ['Created', false], ['InReview', false], ['InProgress', false], ['Archived', false]],
  }
}

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case Types.SORT_BY:
      return {
        ...state,
        filters: {
          ...state.filters,
          sort_by: action.payload.filters,
        }, 
      }
    
    case Types.SORT_BY_STATUS:
      return {
        ...state,
        filters: {
          ...state.filters,
          sort_by_status: action.payload.filters,
        }, 
      }

    default:
      return state;
  }
}

export default reducer;
