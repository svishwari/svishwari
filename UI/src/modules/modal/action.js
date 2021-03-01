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

export {
    showAddDataSource,
    showAddDestination,
    hideModal,
}