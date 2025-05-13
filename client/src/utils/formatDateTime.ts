import {formatDistanceToNow} from "date-fns";
import {uk} from "date-fns/locale";


export function formatDateTime(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleString("uk-UA", {
    dateStyle: "medium",
    timeStyle: "short",
  })
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleString("uk-UA", {
    dateStyle: "medium"
  })
}

export function dateTimeDistanceToNow(dateString: string): string {
  const eventDate = new Date(dateString);
  return formatDistanceToNow(eventDate, {
    addSuffix: true,
    locale: uk,
  })
}