import { configureStore } from '@reduxjs/toolkit'
import counterReducer from '../features/store/reduxExample'
import userReducer from '../features/store/userSlice'

export default configureStore({
  reducer: {
    counter: counterReducer,
    user: userReducer,
  },
})