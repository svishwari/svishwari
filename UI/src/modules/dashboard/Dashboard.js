import React from 'react';
import { connect, useDispatch } from 'react-redux';
import { Box, Button, ListItem, Paper, Typography, IconButton } from '@material-ui/core';
import { Link } from 'react-router-dom';
import CountUp from 'react-countup';
// import DonutChart from 'react-d3-donut/es';
// import CTUSAMap from '../../components/Charts/CTUSAMap';
import { ReactComponent as HomeIllustration } from '../../assets/Home_Illustration.svg';
import HelpCard from '../../assets/images/HelpCard1.png';
import CDPCard from '../../assets/images/HelpCard2.png';
import MarketingCard from '../../assets/images/HelpCard3.png';
import PageTitle from '../../components/PageTitle';
import './Dashboard.scss';
import CTDataGrid from '../../components/Table/CTDataGrid';
import CTPopover from '../../components/Popover/CTPopover';
import { fetchSummaryInfo, fetchRecentSegments } from './store/action';
import CTChip from '../../components/Chip/CTChip';
import HelpResources from '../../components/HelpResources/HelpResources';

const summaryCard = (item, i) => (
  <div className="summary-card" key={`${Math.random().toString(36).substr(2, 36)}`}>
    <div key={i} className="mb-2">
      <span className="iconify" data-icon={`mdi:${item.icon}`} data-inline="false" />
      {`Your ${item.title}`}
    </div>
    <Paper elevation={2} className="paper">
      {item.sections.map((section) => (
        <div className="section" key={`${Math.random().toString(36).substr(2, 36)}`}>
          <CountUp
            start={0}
            end={section.value}
            delay={1}
            formattingFn={(value) => Number(value.toFixed(1)).toLocaleString()}
          />
          <Link to={section.path}>{section.label}</Link>
        </div>
      ))}
    </Paper>
  </div>
);

const Dashboard = (props) => {
  // this hook allows us to access the dispatch function
  const dispatch = useDispatch();

  // Basic Structure of the summary cards data.
  const summaryCards = [
    {
      title: 'Connections',
      icon: 'connection',
      sections: [
        { label: 'Data Sources >', path: '/connections/data-sources', value: 0 },
        { label: 'Destinations >', path: '/connections/destinations', value: 0 },
      ],
    },
    {
      title: 'Customers',
      icon: 'account-details-outline',
      sections: [{ label: 'Customer Profiles >', path: '/customer-profiles', value: 0 }],
    },
    {
      title: 'Orchestration',
      icon: 'account-arrow-right-outline',
      sections: [
        { label: 'Audiences >', path: '/orchestration/audiences', value: 0 },
        { label: 'Segments >', path: '/orchestration/segments', value: 0 },
      ],
    },
  ];

  // Function will be used to map the values from the state post API responses.
  const getSummaryCards = () => {
    if (Object.entries(props.dashboard.summaryInfo).length > 0) {
      summaryCards[0].sections[0].value = props.dashboard.summaryInfo[0].dataSources;
      summaryCards[0].sections[1].value = props.dashboard.summaryInfo[0].destinations;
      summaryCards[1].sections[0].value = props.dashboard.summaryInfo[0].customerProfile;
      summaryCards[2].sections[0].value = props.dashboard.summaryInfo[0].Audiences;
      summaryCards[2].sections[1].value = props.dashboard.summaryInfo[0].Segments;
    }
    return summaryCards;
  };
  const getRecentSegments = () => {
    if (props.dashboard.recentSegments.length > 0) {
      return props.dashboard.recentSegments;
    }
    return [];
  };

  const summaryCardRender = getSummaryCards().map((item, i) => summaryCard(item, i));
  const columns = [
    {
      field: 'name',
      headerName: 'Name',
      flex: 0.4,
      renderCell: (params) => <Link to={() => false}>{params.getValue('name')}</Link>,
    },
    {
      field: 'status',
      headerName: 'Status',
      flex: 0.4,
      renderCell: (params) => {
        const triggerConnection = () => {
          // TODO Call Delivery API
        };
        return (
          <CTChip
            isWorking={params.getValue('status') === 'Delivered'}
            isWorkingFn={triggerConnection}
            isNotWorkingFn={triggerConnection}
          >
            {params.getValue('status') === 'Delivered' ? params.getValue('status') : 'Deliver Now'}
          </CTChip>
        );
      },
    },
    { field: 'size', headerName: 'Size', flex: 0.3 },
    { field: 'created', headerName: 'Created', flex: 0.3 },
    {
      field: 'open',
      headerName: ' ',
      flex: 0.2,
      renderCell: () => (
        <CTPopover
          popoverContent={
            <Box display="flex" flexDirection="column">
              <ListItem>Facebook</ListItem>
              <ListItem>Google</ListItem>
            </Box>
          }
        >
          <Button color="primary" style={{ textTransform: 'capitalize' }}>
            Open in <span className="iconify" data-icon="zmdi-caret-down" data-inline="false" />
          </Button>
        </CTPopover>
      ),
    },
    {
      field: 'extra',
      headerName: ' ',
      flex: 0.1,
      renderCell: () => (
        <CTPopover
          popoverContent={
            <Box display="flex" flexDirection="column">
              <ListItem>Configure</ListItem>
              <ListItem>Remove</ListItem>
            </Box>
          }
        >
          <IconButton>
            <span className="iconify" data-icon="mdi:dots-vertical" data-inline="false" />
          </IconButton>
        </CTPopover>
      ),
    },
  ];
  const helpCards = [
    {
      id:1,
      title: 'Improving human experience with AI',
      description: (
        <Link to="/">
          Read more{' '}
          <span className="iconify" data-icon="mdi:chevron-double-right" data-inline="false" />
        </Link>
      ),
      image: <img src={HelpCard} alt="help" />,
    }, {
      id:2,
      title: 'Realize the potential in your customer data',
      description: (
        <Link to="/">
          Read more{' '}
          <span className="iconify" data-icon="mdi:chevron-double-right" data-inline="false" />
        </Link>
      ),
      image: <img src={CDPCard} alt="help" />,
    }, {
      id: 3,
      title: 'The ABCs of customer data in marketing',
      description: (
        <Link to="/">
          Read more{' '}
          <span className="iconify" data-icon="mdi:chevron-double-right" data-inline="false" />
        </Link>
      ),
      image: <img src={MarketingCard} alt="help" />,
    },
  ];

  React.useEffect(() => {
    dispatch(fetchSummaryInfo());
    dispatch(fetchRecentSegments());
  }, []);
  return (
    <div className="dashboard-wrapper">
      <PageTitle
        title={`Welcome to ${props.userInfo.name}!`}
        welcomePage
        summaryText="Hux is here to help you make better, faster decisions to improve your Customer Experiences."
        readMore="/"
        readMoreLabel="Learn More >"
      >
        <HomeIllustration />
      </PageTitle>
      <div className="content-wrapper">
        <div className="summary">{summaryCardRender}</div>
        <Typography variant="h5" className="recent-heading">
          Recent Segments
        </Typography>
        <CTDataGrid
          autoHeight
          hasStarring={false}
          isTopVisible={false}
          hideFooterPagination
          showTopBar={false}
          headerHeight={0}
          editing={false}
          columns={columns}
          data={getRecentSegments()}
        />
      </div>
      <HelpResources title="Helpful Resources" content={helpCards} />
    </div>
  );
};
const mapStateToProps = (state) => ({
  userInfo: state.user.loggedInUser || [],
  connections: state.connections,
  dashboard: state.dashboard,
  modal: state.modal,
});
export default connect(mapStateToProps)(Dashboard);
