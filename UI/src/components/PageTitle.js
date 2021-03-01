import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Typography, Box, IconButton } from '@material-ui/core';
import { Link } from 'react-router-dom';
import './PageTitle.scss';

const useStyles = makeStyles(() => ({
  FullLayout: {
    background: '#FFFFFF',
    boxShadow: '0px -1px 0px #D0D0CE, 0px 1px 0px #D0D0CE',
    marginTop: '1px',
    padding: '13px 60px 0px 70px',
  },
  FullLayoutHeading: {
    fontFamily: 'Open Sans SemiBold',
    fontSize: '32px',
    fontStyle: 'normal',
    fontWeight: '600',
    lineHeight: '40px',
    letterSpacing: '0.10000000149011612px',
    textAlign: 'left',
  },
  FullLayoutSubHeading: {
    fontFamily: 'Open Sans',
    fontSize: '15px',
    fontStyle: 'normal',
    fontWeight: 'normal',
    lineHeight: '24px',
    letterSpacing: '0.2px',
    marginTop: '8px',
  },
  FullLayoutLeftSection: {
    display: 'flex',
    flexDirection: 'column',
    paddingTop: '17px',
  },
  settings: {
    border: '1px solid #D0D0CE',
    boxSizing: 'border-box',
    borderRadius: '5px',
    width: '45px',
    height: '40px',
  },
}));

const PageTitle = (props) => {
  const classes = useStyles();
  const Layout = (
    <div className="pageTitle">
      {props.children}
      <div className="titleSection">
        <h2>{props.title}</h2>
        <span>
          {props.summaryText}
          <Link to={props.readMore}>{props.readMoreLabel}</Link>
        </span>
      </div>
    </div>
  );
  const FullLayout = (
    <Box display="flex" justifyContent="space-between" className={classes.FullLayout}>
      <div className={classes.FullLayoutLeftSection}>
        <Typography variant="h6" gutterBottom className={classes.FullLayoutHeading}>
          {props.title}
        </Typography>
        <span className={classes.FullLayoutSubHeading}>
          {props.summaryText}
          <Link to={props.readMore}>{props.readMoreLabel}</Link>
        </span>
      </div>
      <div className="FullLayoutChild">{props.children}</div>
      <IconButton aria-label="Settings" className={classes.settings}>
        <span className="iconify" data-icon="mdi:cog" data-inline="false" />
      </IconButton>
    </Box>
  );
  const renderLayout = props.welcomePage ? FullLayout : Layout;
  return renderLayout;
};

export default PageTitle;
