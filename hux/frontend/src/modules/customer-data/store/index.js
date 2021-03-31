const defaultState = {
    customerProfiles: [],
    customerProfile: {},
}

const customerProfileReducer = (state = defaultState, action) => {
    switch (action.type) {
        case "setCustomerProfiles":
            return {
                ...state,
                customerProfiles: [...action.payload] || [],
            };
        case "setCustomerProfile":
            return {
                ...state,
                customerProfile: action.payload || {},
            };
        default:
            return state;
    }
};

export default customerProfileReducer;