import { configureStore } from '@reduxjs/toolkit'
import counterReducer from '../features/reduxExample'

export default configureStore({
  reducer: {
    counter: counterReducer,
  },
})