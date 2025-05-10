"use client";

import {ToastContainer} from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import {CheckCircleIcon, ExclamationCircleIcon} from "@heroicons/react/24/outline";


export default function Toast() {
  return (
    <ToastContainer
      autoClose={5000}
      icon={({type, theme}) => {
        switch (type) {
          case "success":
            return <CheckCircleIcon className="stroke-green-500"/>;
          case "error":
            return <ExclamationCircleIcon className="stroke-red-500"/>;
          default:
            return null;
        }
      }}
    />
  );
}