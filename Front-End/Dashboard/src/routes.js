
import Dashboard from "views/Dashboard.js";
import UserProfile from "views/UserProfile.js";
import Buy_license from "views/Buy_license.js";
import Notifications from "views/Notifications.js";



const dashboardRoutes = [

  {
    path: "/dashboard",
    name: "Dashboard",
    icon: "nc-icon nc-chart-pie-35",
    component: Dashboard,
    layout: "/admin",
  },
  {
    path: "/user",
    name: "User Profile",
    icon: "nc-icon nc-circle-09",
    component: UserProfile,
    layout: "/admin",
  },
  {
    path: "/table",
    name: "Buy license",
    icon: "nc-icon nc-money-coins",
    component: Buy_license,
    layout: "/admin",
  },
  {
    path: "/typography",
    name: "Notifications",
    icon: "nc-icon nc-bell-55",
    component: Notifications,
    layout: "/admin",
  },


];

export default dashboardRoutes;
