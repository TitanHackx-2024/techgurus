import { UserCircleIcon } from "@heroicons/react/24/solid";
import Content from "./pages/Dashboard/content";

const icon = {
  className: "w-5 h-5 text-inherit",
};

export const routes = [
  {
    layout: "dashboard",
    pages: [
      // {
      //   icon: <HomeIcon {...icon} />,
      //   name: "dashboard",
      //   path: "/home",
      //   element: <Home />,
      // },
      {
        icon: <UserCircleIcon {...icon} />,
        name: "content",
        path: "/content",
        element: <Content />,
      },
      // {
      //   icon: <InformationCircleIcon {...icon} />,
      //   name: "notifications",
      //   path: "/notifications",
      //   element: <Notifications />,
      // },
    ],
  },
];

export default routes;
