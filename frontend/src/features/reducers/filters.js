import { Types } from '../actions/type';

const initialState = {
  filters: {
    sort_by: 'Created at'
  }
}

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case Types.SORT_BY:
      return {
        ...state,
        filters: {
          ...state.filters,
          sort_by: action.payload.filters
        }, 
      }

    default:
      return state;
  }
}

export default reducer;
