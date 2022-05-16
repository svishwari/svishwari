const access = {
  admin: {
    audiences: {
      create: true,
      delete: true,
      edit: true,
    },
  },
  editor: {
    audiences: {
      create: true,
      delete: false,
      edit: true,
    },
  },
  viewer: {
    audiences: {
      create: false,
      delete: false,
      edit: false,
    },
  },
}

export default access
