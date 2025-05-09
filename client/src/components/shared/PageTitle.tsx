type PageTitleProps = {
  title: string | undefined;
}

export default function PageTitle({title}: PageTitleProps) {
  if (!title) {
    return null;
  }
  
  return (
    <div className="text-4xl font-sourceSerif text-center mb-5">
      {title}
    </div>
  )
}