import { Types } from '../actions/type';

const initialState = {
  profile: {
    firstName: '',
    lastName: '',
    telephone: '',
    age: '',
    email: '',
    interests: [],
    profileImage: '',
    id: '',
    image_id: '',
  },
  user_token: '',
}

const reducer = (state = initialState, action) => {
    switch (action.type) {
      case Types.LOGIN:
        return {
          ...state,
          user_token: action.payload.user, 
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
      case Types.DISCONNECT:
        return {
          initialState,
        }
      default:
        return state;
    }
  }
  
  export default reducer;