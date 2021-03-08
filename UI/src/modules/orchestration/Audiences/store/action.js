import { getRequest } from "../../../../hooks/apiClient";

const RESOURCE_URL = process.env.REACT_APP_RESOURCE_URL;

const updateAudiences = (payload) => ({
  type: 'updateAudiences',
  payload,
});

const fetchAudiences = () => async (dispatch) => {
  try {
    const response = await getRequest(`${RESOURCE_URL}/audiences`)
    const audiences = response.map(audience => ({
      ...audience,
      ...{
        id: audience.audience_id
      }
    }));
    dispatch(updateAudiences(audiences));
  } catch (error) {
    // TODO: handle error response ...
  }
};

export { fetchAudiences };  // eslint-disable-line import/prefer-default-export
