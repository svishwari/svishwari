const setSegments = (payload) => ({ type: "loadSegments", payload });
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
};