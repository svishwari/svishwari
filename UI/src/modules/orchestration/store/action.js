const setSegments = (payload) => ({ type: "loadSegments", payload });
const setSegmentSummary = (payload) => ({ type: "loadSegmentSummary", payload });
const segmentDelivered = (payload) => ({
    type: "segmentDelivered",
    payload,
});

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

export {
    fetchSegments,
    triggerDeliveredCheck,
    fetchSegmentSummary,
};