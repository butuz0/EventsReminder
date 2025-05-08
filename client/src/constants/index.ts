import {
  UserGroupIcon,
  HomeIcon,
  UserIcon,
  ClipboardDocumentListIcon,
  AcademicCapIcon,
} from "@heroicons/react/24/outline";


export const PriorityOptions = [
  {value: 1, label: "Низький"},
  {value: 2, label: "Середній"},
  {value: 3, label: "Високий"},
  {value: 4, label: "Критичний"},
]

export const NotificationMethods = [
  {value: "email", label: "Email"},
  {value: "tg", label: "Telegram"},
]

export const genderOptions = [
  {value: "m", label: "Чоловік"},
  {value: "f", label: "Жінка"},
  {value: "o", label: "Інша"}
];

export const RecurrenceRuleOptions = [
  {value: "d", label: "Щодня"},
  {value: "w", label: "Щотижня"},
  {value: "m", label: "Щомісяця"},
  {value: "y", label: "Щороку"},
]

export const LeftNavbarLinks = [
  {
    label: "Головна",
    href: "/home",
    icon: HomeIcon
  },
  {
    label: "Профіль",
    href: "/profile",
    icon: UserIcon
  },
  {
    label: "Події",
    href: "/events",
    icon: ClipboardDocumentListIcon
  },
  {
    label: "Команди",
    href: "/teams",
    icon: UserGroupIcon
  },
  {
    label: "Університет",
    href: "/university",
    icon: AcademicCapIcon
  }
]