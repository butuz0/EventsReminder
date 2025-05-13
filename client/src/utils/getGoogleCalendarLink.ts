import {Event} from "@/types";


export default function getGoogleCalendarLink(event: Event) {
  const {
    title,
    description,
    start_datetime,
    location
  } = event;
  
  const date = new Date(start_datetime).toISOString().replace(/[-:]|\.\d{3}/g, "");
  
  const params = new URLSearchParams({
    action: "TEMPLATE",
    text: title,
    dates: `${date}/${date}`,
    details: description || "",
    location: location || "",
  });
  
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}