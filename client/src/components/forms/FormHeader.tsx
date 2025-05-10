import Link from "next/link";

type FormHeaderProps = {
  title?: string;
  staticText?: string;
  linkText?: string;
  linkHref?: string;
};


export default function FormHeader(
  {
    title,
    staticText,
    linkHref,
    linkText,
  }: FormHeaderProps) {
  return (
    <div className="px-4 sm:mx-auto sm:w-full sm:max-w-md sm:px-6 pb-5">
      <h2 className="text-xl font-semibold mt-3 text-center">
        {title}
      </h2>
      {(staticText || linkText) && linkHref && (
        <p className="mt-2 text-center text-md">
          {staticText && <span>{staticText}</span>}
          {linkText && (
            <Link
              href={linkHref}
              className="ml-1 font-semibold text-blue-600
              hover:text-blue-400"
            >
              {linkText}
            </Link>
          )}
        </p>
      )}
    </div>
  );
}