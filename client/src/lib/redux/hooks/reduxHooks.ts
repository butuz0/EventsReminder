import type {AppStore, RootState, AppDispatch} from "@/lib/redux/store";
import type {TypedUseSelectorHook} from "react-redux";
import {useDispatch, useSelector, useStore} from "react-redux";


export const useAppStore: () => AppStore = useStore;
export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
