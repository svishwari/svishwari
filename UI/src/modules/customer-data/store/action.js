const setCustomerProfiles = (payload) => ({ type: "setCustomerProfiles", payload });
const setCustomerProfile = (payload) => ({ type: "setCustomerProfile", payload });

const fetchCustomerProfiles = () => async (dispatch) => {
    await new Promise((done) => setTimeout(() => done(), 2000));
    // #TODO
    // Fetch List of customers
    const response = [
        {
            id: "1",
            customerID: "1",
            customerProfile: "M",
            customerName: "Cooper, Kristin",
            customerEmail: "tanya.hill@example.com",
            customerPhone: "(205) 555-0100",
            accountNumber: "123198091849812301-2039-12",
            customerValue: "Medium",
            customerEvents: 5,
        },
        {
            id: "2",
            customerID: "2",
            customerProfile: "F",
            customerName: "Cooper, Kristin",
            customerEmail: "tanya.hill@example.com",
            customerPhone: "(205) 555-0100",
            accountNumber: "123198091849812301-2039-12",
            customerValue: "High",
            customerEvents: 5,
        },
        {
            id: "3",
            customerID: "3",
            customerProfile: "M",
            customerName: "Cooper, Kristin",
            customerEmail: "tanya.hill@example.com",
            customerPhone: "(205) 555-0100",
            accountNumber: "123198091849812301-2039-12",
            customerValue: "Low",
            customerEvents: 5,
        },
        {
            id: "4",
            customerID: "4",
            customerProfile: "F",
            customerName: "Cooper, Kristin",
            customerEmail: "tanya.hill@example.com",
            customerPhone: "(205) 555-0100",
            accountNumber: "123198091849812301-2039-12",
            customerValue: "High",
            customerEvents: 5,
        },
        {
            id: "5",
            customerID: "5",
            customerProfile: "M",
            customerName: "Cooper, Kristin",
            customerEmail: "tanya.hill@example.com",
            customerPhone: "(205) 555-0100",
            accountNumber: "123198091849812301-2039-12",
            customerValue: "High",
            customerEvents: 5,
        },
    ];
    dispatch(setCustomerProfiles(response));
};

const fetchCustomerProfile = () => async (dispatch) => {
    await new Promise((done) => setTimeout(() => done(), 2000));
    // #TODO
    // Fetch specific customer details based on id
    const response = {
        id: "1",
        customerID: "1",
        customerProfile: "M",
        customerName: "Cooper, Kristin",
        customerEmail: "tanya.hill@example.com",
        customerPhone: "(205) 555-0100",
        accountNumber: "123198091849812301-2039-12",
        customerValue: "Medium",
        customerEvents: 5,
        events: [
            {
                id: "1",
                eventType: "Subscription Expiration SMS",
                charge: 10.23,
                date: "8/23/20 11:59PM",
            },
            {
                id: "2",
                eventType: "Subscription Expiration SMS",
                charge: 10.23,
                date: "8/23/20 11:59PM",
            },
            {
                id: "3",
                eventType: "Subscription Expiration SMS",
                charge: 10.23,
                date: "8/23/20 11:59PM",
            },
        ],
        includedIn: [
            {
                id: "1",
                orchestrationName: "Audience Name",
                connectionStatus: "Connected",
            },
            {
                id: "2",
                orchestrationName: "Audience Name",
                connectionStatus: "Connected",
            },
            {
                id: "3",
                orchestrationName: "Audience Name",
                connectionStatus: "Connected",
            },
        ],
        dataSources: [
            {
                id: "1",
                fileName: "Name",
                source: "Client",
                lastUpdated: "8/23/20 11:59PM",
                stitched: 21,
                pinned: 34,
            },
            {
                id: "2",
                fileName: "Name",
                source: "Client",
                lastUpdated: "8/23/20 11:59PM",
                stitched: 21,
                pinned: 34,
            },
        ],
    };
    dispatch(setCustomerProfile(response));
};

export {
    fetchCustomerProfiles,
    fetchCustomerProfile
};

// #TODO
// Fetch summary of list of customer
// Values like Records, Data Sources, Stitches, Pinned, Avg. Strength

// #TODO
// Fetch summary of specific customer 
// Values like Customer Length, Strength, Last Event, Value, Conversion Time