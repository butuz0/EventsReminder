"use client";

import React, {useEffect, useState} from "react";
import {useGetAllFacultiesQuery, useGetFacultyDepartmentsQuery} from "@/lib/redux/slices/units/unitsApiSlice";
import {FieldValues, UseFormReturn} from "react-hook-form";
import SelectFieldComponent from "@/components/forms/SelectFieldComponent";
import Select from "react-select";
import ClientOnlyComponent from "@/utils/ClientOnlyComponent";
import {FormLabel} from "@/components/ui/form";
import {selectFieldStyles} from "@/components/forms/selectFieldStyles";

interface DepartmentSelectFieldProps<T extends FieldValues = any> {
  form: UseFormReturn<T>;
  placeholder?: string;
}

interface Option {
  value: number;
  label: string;
}

export default function DepartmentSelectField({form}: DepartmentSelectFieldProps) {
  const [facultyOptions, setFacultyOptions] = useState<Option[]>([]);
  const [departmentOptions, setDepartmentOptions] = useState<Option[]>([]);
  const [selectedFaculty, setSelectedFaculty] = useState<number | undefined>(undefined);
  
  const {data: facultiesData, isLoading: facultiesLoading} = useGetAllFacultiesQuery();
  const {data: departmentsData, isLoading: departmentsLoading} = useGetFacultyDepartmentsQuery(
    selectedFaculty!, {
      skip: !selectedFaculty,
    });
  
  // set faculties select options when faculties are loaded
  useEffect(() => {
    if (facultiesData?.faculties?.results) {
      setFacultyOptions(
        facultiesData.faculties.results.map((f) => ({
          value: f.id,
          label: f.faculty_name,
        }))
      );
    }
  }, [facultiesData]);
  
  // set department select options once the user has chosen the faculty
  useEffect(() => {
    if (!selectedFaculty) {
      setDepartmentOptions([]);
      return;
    }
    
    const departments = departmentsData?.departments.results.map(
      (department) => (
        {
          value: department.id,
          label: department.department_name,
        }
      )) ?? [];
    
    setDepartmentOptions(departments);
  }, [selectedFaculty, departmentsData]);
  
  function facultiesOnChange(value: number | undefined) {
    setSelectedFaculty(value);
  }
  
  return (
    <div className="space-y-5">
      <div className="space-y-1">
        <FormLabel>Факультет</FormLabel>
        {/*<ClientOnlyComponent>*/}
        <Select
          options={facultyOptions}
          isLoading={facultiesLoading}
          isDisabled={facultiesLoading}
          onChange={(selected) => facultiesOnChange((selected as Option)?.value)}
          value={facultyOptions.find((option) => option.value === selectedFaculty)}
          placeholder="Оберіть Ваш факультет"
          styles={selectFieldStyles}
        />
        {/*</ClientOnlyComponent>*/}
      </div>
      <SelectFieldComponent
        form={form}
        name="department"
        label="Кафедра"
        options={departmentOptions}
        isDisabled={!selectedFaculty || departmentsLoading}
        isLoading={departmentsLoading}
        placeholder={!selectedFaculty
          ? "Спочатку оберіть Ваш факультет"
          : departmentsLoading
            ? "Завантаження кафедр..."
            : "Оберіть Вашу кафедру"}
      />
    </div>
  )
}