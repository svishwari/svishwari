import React from 'react';
import { Link } from 'react-router-dom';
import DonutChart from 'react-d3-donut';
import { Box, Button, IconButton, ListItem, Typography } from '@material-ui/core';
import { ReactComponent as TitleImage } from '../../assets/OrchestrationTitle.svg';
import CTNewList from '../../components/List/CTNewList';
import PageTitle from '../../components/PageTitle';
import './OrchestrationSummary.scss';
import CTUSAMap from '../../components/Charts/CTUSAMap';
import CTList from '../../components/List/List';
import CTChip from '../../components/Chip/CTChip';
import CTPopover from '../../components/Popover/CTPopover';

const lists = {
  audiences: [
    { id: 1, title: '⭐️ Audience Name' },
    { id: 2, title: '⭐️ Audience Name' },
    { id: 3, title: '⭐️ Audience Name' },
    { id: 4, title: '⭐️ Audience Name' },
    { id: 5, title: '⭐️ Audience Name' },
  ],
  audiencesDonuts: [
    {
      id: 1,
      title: 'Devices',
      data: [
        { name: 'Device1', count: 10, color: '#00A99D' },
        { name: 'Device2', count: 30, color: '#E89F74' },
        { name: 'Device3', count: 60, color: '#DA5B41' },
      ],
    },
    {
      id: 2,
      title: 'Devices',
      data: [
        { name: 'Device1', count: 10, color: '#00A99D' },
        { name: 'Device2', count: 30, color: '#E89F74' },
        { name: 'Device3', count: 60, color: '#DA5B41' },
      ],
    },
    {
      id: 3,
      title: 'Devices',
      data: [
        { name: 'Device1', count: 10, color: '#00A99D' },
        { name: 'Device2', count: 30, color: '#E89F74' },
        { name: 'Device3', count: 60, color: '#DA5B41' },
      ],
    },
  ],
  states: [{ WA: 90 }, { NY: 90 }, { MT: 90 }, { NY: 28 }, { CA: 18 }, { TX: 90 }],
  stateList: [
    {
      id: 1,
      name: 'Washington',
      value: '50%',
    },
    {
      id: 2,
      name: 'New York',
      value: '48%',
    },
    {
      id: 3,
      name: 'Montana',
      value: '48%',
    },
    {
      id: 4,
      name: 'New York',
      value: '48%',
    },
    {
      id: 5,
      name: 'California',
      value: '48%',
    },
    {
      id: 6,
      name: 'Texas',
      value: '48%',
    },
  ],
  audienceSummary: [
    {
      id: 1,
      name: 'Audience Name',
      status: 'Delivered',
      size: '1.2 Million',
      created: '8/23/20 11:59PM',
      open: '',
      extra: '',
    },
    {
      id: 2,
      name: 'Audience Name',
      status: 'Delivered',
      size: '1.2 Million',
      created: '8/23/20 11:59PM',
      open: '',
      extra: '',
    },
    {
      id: 3,
      name: 'Audience Name',
      status: 'Delivered',
      size: '1.2 Million',
      created: '8/23/20 11:59PM',
      open: '',
      extra: '',
    },
  ],
  segmentSummaryColumns: [
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
            onClickFunc={triggerConnection}
          >
            {params.getValue('status') === 'Delivered' ? params.getValue('status') : 'Not Delivered'}
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
              <Button>
                <span className="iconify" data-icon="logos:facebook" data-inline="false" />
                {'\u00A0'}Facebook
              </Button>
              <Button>
                <span className="iconify" data-icon="logos:google-analytics" data-inline="false" />
                {'\u00A0'}Google
              </Button>
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
  ],
  segmentsSummaryRows: [
    {
      id: 1,
      name: 'Segment Name',
      status: 'Delivered',
      size: '1.2 Million',
      created: '8/23/20 11:59PM',
      open: '',
      extra: '',
    },
    {
      id: 2,
      name: 'Segment Name',
      status: 'Delivered',
      size: '1.2 Million',
      created: '8/23/20 11:59PM',
      open: '',
      extra: '',
    },
    {
      id: 3,
      name: 'Segment Name',
      status: 'Not Delivered',
      size: '1.2 Million',
      created: '8/23/20 11:59PM',
      open: '',
      extra: '',
    },
  ],
};

const OrchestrationSummary = () => {
  const triggerAdd = (name) => {
    console.log(name);
  };
  const insightCard = (section) => (
    <div className="insight-wrap">
      <div className="section-title">
        <h3 className="title">
          <Link to="/connections/data-sources">{`${section.name}s Overview >`}</Link>
        </h3>
        <span
          className="action-link"
          onKeyPress={() => triggerAdd(section.name)}
          onClick={() => triggerAdd(section.name)}
        >
          {`+ ${section.name}`}
        </span>
      </div>
      <div className="infographic-section">
        <div className="donuts">
          <div className="count">
            {section.count}
            <span>{`${section.name}s`}</span>
          </div>
          <div className="donut-wrap">
            {lists.audiencesDonuts.map((chart) => (
              <DonutChart
                innerRadius={30}
                key={`--${chart.id}`}
                outerRadius={40}
                transition
                svgClass="example6"
                pieClass="pie6"
                displayTooltip={false}
                strokeWidth={2}
                data={chart.data}
              />
            ))}
          </div>
        </div>
        <div className="list">
          <CTNewList
            style={{ flex: 1 }}
            items={lists.audiences}
            showHeading
            heading="STARRED AUDIENCES"
          />
        </div>
        <div className="worldmap">
          <CTUSAMap data={lists.states} />
        </div>
        <div className="table">
          <CTList
            columns={[
              {
                field: 'name',
                headerName: 'Name',
                flex: 0.7,
              },
              {
                field: 'value',
                headerName: 'Value',
                flex: 0.3,
              },
            ]}
            rows={lists.stateList}
          />
        </div>
      </div>
    </div>
  );
  return (
    <>
      <PageTitle
        title="Orchestration"
        summaryText="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean odio malesuada cursus est. Arcu semper aliquam diam volutpat nunc, quam."
        readMore="/"
        readMoreLabel="Learn More"
      >
        <TitleImage />
      </PageTitle>
      <div className="summary-wrapper">
        {insightCard({
          name: 'Segment',
          count: 3,
        })}
        <div className="recentSegments">
          <Typography variant="h5" className="heading">
            Recent Segments
          </Typography>
          <CTList columns={lists.segmentSummaryColumns} rows={lists.segmentsSummaryRows} />
        </div>
      </div>
    </>
  );
};

export default OrchestrationSummary;
