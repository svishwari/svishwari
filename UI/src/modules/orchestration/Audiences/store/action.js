import { getRequest } from "../../../../hooks/apiClient";

const RESOURCE_URL = process.env.REACT_APP_RESOURCE_URL;

const updateAudiences = (payload) => ({
  type: 'updateAudiences',
  payload,
});

const fetchAudiences = () => async (dispatch) => {
  const response = await getRequest(`${RESOURCE_URL}/audiences`)
  const audiences = response.map(audience => ({
      id: audience.audience_id,
      name: audience.audience_name,
    }
  ));
  dispatch(updateAudiences(audiences));
};

export { fetchAudiences };  // eslint-disable-line import/prefer-default-export
