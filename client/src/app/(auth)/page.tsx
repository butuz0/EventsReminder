import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center gap-6">
      <p className="text-center text-lg">
        Вітаємо! Керуйте подіями та нагадуваннями у
        своєму університетському житті легко та зручно.
      </p>
      
      <div className="flex w-full flex-col gap-3">
        <Link
          href="/register"
          className="w-full rounded-lg bg-[#4d4dff] px-6 py-3
          text-center text-lg font-medium text-white shadow-md
          transition hover:bg-[#5663e6]"
        >
          Зареєструватись
        </Link>
        
        <p className="text-center text-md text-gray-800">
          Вже маєте акаунт?
        </p>
        
        <Link
          href="/login"
          className="w-full rounded-lg border border-blue-600
          px-6 py-3 text-center text-lg font-medium text-blue-600
          transition hover:bg-blue-50"
        >
          Увійти
        </Link>
      </div>
    </div>
  );
}
