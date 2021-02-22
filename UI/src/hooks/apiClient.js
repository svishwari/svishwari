import axios from "axios";

const headers = {
  "Content-Type": "application/json",
};

axios.interceptors.request.use(
  (request) => {
    request.headers = headers;
    return request;
  },
  (error) => Promise.reject(error)
);

axios.interceptors.response.use(
  (response) => response,
  (error) => Promise.reject(error)
);
export const postRequest = async (url, payload = {}) => {
  const data = await axios
    .post(url, payload)
    .then((resp) => resp.data)
    .catch((err) => ({ error: err.response.data }));
  return data;
};

export const putRequest = async (url, payload = {}) => {
  const data = await axios
    .put(url, payload)
    .then((resp) => resp.data)
    .catch((err) => ({ error: err.response.data }));
  return data;
};

export const getRequest = async (url) => {
  const data = await axios
    .get(url)
    .then((resp) => resp.data)
    .catch((err) => ({ error: err.response.data }));
  return data;
};

export const deleteRequest = async (url) => {
  const data = await axios
    .delete(url)
    .then((resp) => resp.data)
    .catch((err) => ({ error: err.response.data }));
  return data;
};
