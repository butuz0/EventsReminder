import {configureStore} from "@reduxjs/toolkit";
import {baseApiSlice} from "@/lib/redux/slices/baseApiSlice";
import {setupListeners} from "@reduxjs/toolkit/query";
import {rootReducer} from "@/lib/redux/slices/rootReducer";

export const makeStore = () => {
  return configureStore({
    reducer: rootReducer,
    middleware: (getDefaultMiddleware) =>
      getDefaultMiddleware().concat(baseApiSlice.middleware),
    devTools: process.env.NODE_ENV !== "production",
  });
};

setupListeners(makeStore().dispatch);

export type AppStore = ReturnType<typeof makeStore>;
export type RootState = ReturnType<AppStore["getState"]>;
export type AppDispatch = AppStore["dispatch"];
