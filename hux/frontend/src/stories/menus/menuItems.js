export default [
  {
    icon: "mdi-home-outline",
    name: "Menu Item 1",
    action: () => {},
  },
  { icon: "mdi-bullhorn-outline", name: "Menu Item 2" },
  {
    name: "Sub 1",
    menu: [
      { icon: "mdi-home-outline", name: "1.1" },
      { icon: "mdi-bullhorn-outline", name: "1.2" },
      {
        name: "Sub-menu 2",
        menu: [
          { name: "2.1" },
          { name: "2.2" },
          {
            name: "Sub-menu 3",
            menu: [{ name: "3.1" }, { name: "3.2" }],
          },
        ],
      },
    ],
  },

  { icon: "mdi-flip-h mdi-account-plus-outline", name: "Menu Item 3" },
  {
    icon: "mdi-tune-vertical-variant",
    name: "Menu Item 4",
    action: () => {},
  },
  {
    icon: "mdi-account-details-outline",
    name: "Menu Item 5",
    action: () => {},
  },
]
