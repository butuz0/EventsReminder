import {MagnifyingGlassIcon} from "@heroicons/react/24/outline";

interface SearchProps {
  placeholder?: string;
}


export default function Search({placeholder = "Пошук..."}: SearchProps) {
  return (
    <div className="relative w-full">
      <input
        type="text"
        className="w-full rounded-md border border-gray-200 shadow-sm
        bg-white pl-10 pr-3 py-2 text-sm placeholder:text-gray-600
        focus:outline-none focus:border-blue-500
        "
        placeholder={placeholder}
      />
      <MagnifyingGlassIcon
        className="absolute left-3 top-1/2 w-5
        -translate-y-1/2 text-gray-400"
      />
    </div>
  );
}
