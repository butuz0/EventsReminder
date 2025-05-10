import {baseApiSlice} from "@/lib/redux/slices/baseApiSlice";
import authReducer from "@/lib/redux/slices/auth/authSlice";


export const rootReducer = {
  [baseApiSlice.reducerPath]: baseApiSlice.reducer,
  auth: authReducer,
};