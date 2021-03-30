// import { getRequest } from "../../../hooks/apiClient";
// import slugs from "../../../resources/slugs";

const setSummary = (payload) => ({ type: 'loadSummary', payload });

const updateRecentSegments = (payload) => ({
  type: 'updateRecentSegments',
  payload,
});

// Methods
const fetchSummaryInfo = () => async (dispatch) => {
  // #TODO
  // Fetch summary/no of datasource,destinations etc.
  await new Promise((done) => setTimeout(() => done(), 500));
  const response = [
    {
      dataSources: 53,
      destinations: 3,
      customerProfile: 530000,
      Audiences: 53,
      Segments: 3,
    },
  ];
  dispatch(setSummary(response));
};
const fetchRecentSegments = () => async (dispatch) => {
  await new Promise((done) => setTimeout(() => done(), 1200));
  // #TODO
  // Fetch only a limited no of segments (if user has created any)
  const response = [
    {
      id: Math.random().toString(36).substr(2, 36),
      name: 'Social Medial Campaign',
      status: "Delivered",
      size: '1.2 M',
      created: '8/23/20 11:59PM',
      open: '',
      extra: '',
    },
    {
      id: Math.random().toString(36).substr(2, 36),
      name: 'Branding Campaign',
      status: "Delivered",
      size: '1.3 M',
      created: '8/23/20 11:59PM',
      open: '',
      extra: '',
    },
    {
      id: Math.random().toString(36).substr(2, 36),
      name: 'Customer Comeback',
      status: "Not Delivered",
      size: '1.75 M',
      created: '8/23/20 11:59PM',
      open: '',
      extra: '',
    },
  ];
  dispatch(updateRecentSegments(response));
};

export { fetchSummaryInfo, fetchRecentSegments };

// #TODO
// Fetch only a limited no of audiences (if user has created any)
