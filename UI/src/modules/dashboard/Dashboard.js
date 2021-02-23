import React from 'react';
import { connect } from 'react-redux';
import { Paper, Typography } from '@material-ui/core';
import { Link } from 'react-router-dom';
import CountUp from 'react-countup';
// import DonutChart from 'react-d3-donut/es';
// import CTUSAMap from '../../components/Charts/CTUSAMap';
import { ReactComponent as HomeIllustration } from '../../assets/Home_Illustration.svg';
import PageTitle from '../../components/PageTitle';
import './Dashboard.scss';
import CTDataGrid from '../../components/Table/CTDataGrid';

const Dashboard = (props) => {
  const summaryCards = [
    {
      title: 'Connections',
      icon: 'connection',
      sections: [
        { label: 'Data Sources >', path: '/connections/dataSources', value: 53 },
        { label: 'Destinations >', path: '/connections/destinations', value: 3 },
      ],
    },
    {
      title: 'Customers',
      icon: 'account-details-outline',
      sections: [{ label: 'Customer Profiles >', path: '/connections/dataSources', value: 530000 }],
    },
    {
      title: 'Orchestration',
      icon: 'account-arrow-right-outline',
      sections: [
        { label: 'Audiences >', path: '/connections/dataSources', value: 53 },
        { label: 'Segments >', path: '/connections/destinations', value: 3 },
      ],
    },
  ];
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
  const summaryCardRender = summaryCards.map((item, i) => summaryCard(item, i));
  const columns = [
    {
      field: 'name',
      headerName: 'Name',
      flex: 0.8,
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 250,
    },
    { field: 'size', headerName: 'Size', flex: 0.4 },
    { field: 'created', headerName: 'Created', flex: 0.6 },
    {
      field: 'open',
      headerName: ' ',
      flex: 0.4,
    },
    {
      field: 'extra',
      headerName: ' ',
      flex: 0.3,
    },
  ];
  const rows = [
    {
      name: 'Audience Name',
      status: 'Delivered.',
      size: '1.2M',
      created: '8/23/20 11:59PM',
      delivered: true,
      starred: true,
      draft: false,
      id: 1,
    },
  ];
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
        <Typography variant="h5">Recent Segments</Typography>
        <CTDataGrid
          autoHeight
          hasStarring
          hideFooterPagination
          showTopBar={false}
          headerHeight={0}
          editing={false}
          columns={columns}
          rows={rows}
        />
      </div>
    </div>
  );
};
const mapStateToProps = (state) => ({
  userInfo: state.user.loggedInUser || [],
  connections: state.connections,
});
export default connect(mapStateToProps)(Dashboard);
