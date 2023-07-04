import { configureStore } from '@reduxjs/toolkit'

import profile from '../reducers/profile';

const store = configureStore({
  reducer: {
    user: profile,
  },
})

export default store;