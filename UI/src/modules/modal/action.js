const addDataSourceLoad = (props={}) => ({
    type: "SHOW_MODAL",
    modalType: "OPEN_ADD_DATA_SOURCE",
    modalProps: props,
});

const addDestinationLoad = (props={}) => ({
    type: "SHOW_MODAL",
    modalType: "OPEN_ADD_DESTINATION",
    modalProps: props,
});

const addSegmentLoad = (props={}) => ({
    type: "SHOW_MODAL",
    modalType: "OPEN_ADD_SEGMENT",
    modalProps: props,
});

const showFetchScore = (props={}) => ({
    type: "SHOW_MODAL",
    modalType: "SHOW_FETCH_SCORE",
    modalProps: props,
})

const closeModal = () => ({
    type: "HIDE_MODAL"
});

const hideModal = () => async (dispatch) => {
    dispatch(closeModal());
};

const showAddDestination = (props) => async (dispatch) => {
    dispatch(addDestinationLoad(props));
};

const showAddDataSource = (props) => async (dispatch) => {
    dispatch(addDataSourceLoad(props));
};

const showAddSegment = (props) => async (dispatch) => {
    dispatch(addSegmentLoad(props));
};

export {
    showAddDataSource,
    showAddDestination,
    showAddSegment,
    showFetchScore,
    hideModal,
}