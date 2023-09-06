import { Types } from './type';

export const FiltersActions = {
  sortBy: (filters) => ({
    type: Types.SORT_BY, payload: {filters}
  }),

  sortByStatus: (filters) => ({
    type: Types.SORT_BY_STATUS, payload: {filters}
  })
}