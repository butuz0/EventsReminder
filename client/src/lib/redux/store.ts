import {configureStore} from "@reduxjs/toolkit";
import {baseApiSlice} from "@/lib/redux/slices/baseApiSlice";

export const makeStore = () => {
  return configureStore({
    reducer: {
      [baseApiSlice.reducerPath]: baseApiSlice.reducer,
    },
    middleware: (getDefaultMiddleware) =>
      getDefaultMiddleware().concat(baseApiSlice.middleware),
    devTools: process.env.NODE_ENV !== "production",
  });
};

export type AppStore = ReturnType<typeof makeStore>;
export type RootState = ReturnType<AppStore["getState"]>;
export type AppDispatch = AppStore["dispatch"];
