import {getRequest} from "../../../hooks/apiClient";

const RESOURCE_URL = process.env.REACT_APP_RESOURCE_URL;

const setAudiences = (payload) => ({
    type: "loadAudiences",
    payload,
});

const setSegments = (payload) => ({
    type: "loadSegments",
    payload
});

const setAddSegments = (payload) => ({
    type: "addSegment",
    payload
});

const setRemoveSegment = (payload) => ({
    type: "removeSegment",
    payload
});

const setSegmentSummary = (payload) => ({
    type: "loadSegmentSummary",
    payload
});

const segmentDelivered = (payload) => ({
    type: "segmentDelivered",
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
        dispatch(setAudiences(audiences));
    } catch (error) {
        // TODO: handle error response ...
    }
};

const fetchSegments = () => async (dispatch) => {
    await new Promise((done) => setTimeout(() => done(), 2000));
    const response = [
        {
            id: "1",
            segmentName: "Segment Name 1",
            deliverStatus: "Not Delivered",
            models: ["Churn"],
            size: "1.2M",
            created: "12/07/19 01:21PM",
        },
        {
            id: "2",
            segmentName: "Segment Name 2",
            deliverStatus: "Delivered",
            models: ["Churn","Propensity"],
            size: "1.2M",
            created: "12/07/19 01:21PM",
        },
        {
            id: "3",
            segmentName: "Segment Name 3",
            deliverStatus: "Delivered",
            models: ["Churn"],
            size: "1.2M",
            created: "12/07/19 01:21PM",
        },
    ];

    dispatch(setSegments(response));
};

const addSegment = (selectedModels) => async (dispatch) => {
    const response = {
        id: "5",
        segmentName: "Segment Name 5",
        deliverStatus: "Not Delivered",
        models: selectedModels,
        size: "1.2M",
        created: "12/07/19 01:21PM",
    };
    dispatch(setAddSegments(response));
};

const removeSegment = (id) => async (dispatch) => {
    dispatch(setRemoveSegment({id}));
}

const fetchSegmentSummary = () => async (dispatch) => {
    await new Promise((done) => setTimeout(() => done(), 2000));
    const response = {
        segmentName: "Segment Name 1",
        created: "1/12/2020 • 15:32",
        models: ["Churn"],
        destinations: [
            {
              id: "602ec30dc920d42f1c4c5d22",
              destination: "fb",
              status: "Not Connected",
              destinationName: "File Name 1",
              account: "Pendleton",
              lastUpdated: "03/26/19 05:04PM",
            },
            {
              id: "602ec30e3d14a94dc1f30e97",
              destination: "ga",
              status: "Not Connected",
              destinationName: "File Name 2",
              account: "Pendleton",
              lastUpdated: "03/26/19 05:04PM",
            },
            {
              id: "602ec30ed4a16f2941a2e37a",
              destination: "sfmc",
              status: "Not Connected",
              destinationName: "File Name 3",
              account: "Pendleton",
              lastUpdated: "03/26/19 05:04PM",
            },
        ],
        customers: [
            {
                id: "1",
                customerName: "Brooklyn Simmons",
                results: "High",
                device: "Mobile",
                age: "21",
                gender: "F",
                incomeRange: "25000$",
            },
            {
                id: "2",
                customerName: "Brooklyn Simmons",
                results: "High",
                device: "Mobile",
                age: "21",
                gender: "F",
                incomeRange: "25000$",
            },
            {
                id: "3",
                customerName: "Brooklyn Simmons",
                results: "High",
                device: "Mobile",
                age: "21",
                gender: "F",
                incomeRange: "25000$",
            },
        ],
    };
    dispatch(setSegmentSummary(response));
};

const triggerDeliveredCheck = (id) => async (dispatch) => {
    await new Promise((done) => setTimeout(() => done(), 3000));
    const response = {
      id,
      status: "Delivered",
    };
    dispatch(segmentDelivered(response));
};

const addDraftSegment = (selectedModels) => async (dispatch) => {
    const response = {
        id: "10",
        models: selectedModels,
        isDraft: true,
        created: "12/07/19 01:21PM",
    };
    dispatch(setAddSegments(response));
};

export {
    fetchAudiences,
    addSegment,
    addDraftSegment,
    removeSegment,
    fetchSegments,
    triggerDeliveredCheck,
    fetchSegmentSummary,
};
