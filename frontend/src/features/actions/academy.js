import { Types } from "./type";

export const AcademyActions = {
    setAcademy: (academy) => ({
        type: Types.SET_ACADEMY, payload: { academy }
    }),
}