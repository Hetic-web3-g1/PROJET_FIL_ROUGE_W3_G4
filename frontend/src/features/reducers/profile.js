import { Types } from '../constants/actionTypes';

const initialState = {
  profile: {
    firstName: '',
    lastName: '',
    telephone: '',
    age: 66,
    email: '',
    interests: [],
    profileImage: '',
  },
}

const reducer = (state = initialState, action) => {
    switch (action.type) {
      case Types.LOGIN:
      console.log('login', action.payload.user)
        return {
          ...state,
          profile: action.payload.user, 
        }
      case Types.UPDATE_USER:
        return {
          ...state,
          profile: action.payload.user,
        }
      case Types.UPDATE_PROFILE_PICTURE:
        return {
          ...state,
          profile: {
            ...state.profile,
            profileImage: action.payload.image
          }
        }
      default:
        return state;
    }
  }
  
  export default reducer;