import { Types } from "../actions/type";

const initialState = {
    academy: {
        name: '',
        id: '',
        created_at: '',
        updated_at: '',
    }
}

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case Types.SET_ACADEMY:
            return {
                ...state,
                academy: action.payload.academy
            }

        default:
            return state;
    }
}

export default reducer;