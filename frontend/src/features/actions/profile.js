import { Types } from '../constants/actionTypes';

export const ProfileActions = {
    updateProfileImage: (image) => ({ type: Types.UPDATE_PROFILE_PICTURE, payload: { image } }),  
    updateProfile: (user) => ({ type: Types.UPDATE_USER, payload: { user } }),  
    login: (user) => ({ type: Types.LOGIN, payload: { user } })
}