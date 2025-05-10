"use client";

import React, {useState} from "react";
import {EyeIcon, EyeSlashIcon} from "@heroicons/react/24/outline";
import {Input} from "@/components/ui/input";

export interface PasswordInputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
}

const PasswordInput = React.forwardRef<HTMLInputElement, PasswordInputProps>(
  ({className, ...props}, ref) => {
    const [visible, setVisible] = useState(false);
    
    const toggleVisibility = () => setVisible((prev) => !prev);
    
    const VisibilityIcon = visible ? EyeIcon : EyeSlashIcon;
    
    return (
      <div className="flex w-full items-center gap-2">
        <Input
          type={visible ? "text" : "password"}
          ref={ref}
          className={`pr-10 ${className}`}
          {...props}
        />
        <VisibilityIcon
          onClick={toggleVisibility}
          className="w-7 hover:cursor-pointer"/>
      </div>
    );
  }
);

PasswordInput.displayName = "PasswordInput";

export {PasswordInput};
