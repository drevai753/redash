import React from "react";
import PropTypes from "prop-types";
import Dropdown from "antd/lib/dropdown";
import Menu from "antd/lib/menu";
import Button from "antd/lib/button";
import PlainButton from "@/components/PlainButton";
import { clientConfig } from "@/services/auth";

import PlusCircleFilledIcon from "@ant-design/icons/PlusCircleFilled";
import ShareAltOutlinedIcon from "@ant-design/icons/ShareAltOutlined";
import FileOutlinedIcon from "@ant-design/icons/FileOutlined";
import FileExcelOutlinedIcon from "@ant-design/icons/FileExcelOutlined";
import EllipsisOutlinedIcon from "@ant-design/icons/EllipsisOutlined";

import QueryResultsLink from "./QueryResultsLink";

export default function QueryControlDropdown(props) {
  const menu = (
    <Menu>
      {!props.query.isNew() && (!props.query.is_draft || !props.query.is_archived) && (
        <Menu.Item>
          <PlainButton onClick={() => props.openAddToDashboardForm(props.selectedTab)}>
            <PlusCircleFilledIcon /> Add to Dashboard
          </PlainButton>
        </Menu.Item>
      )}
      {!clientConfig.disablePublicUrls && !props.query.isNew() && (
        <Menu.Item>
          <PlainButton
            onClick={() => props.showEmbedDialog(props.query, props.selectedTab)}
            data-test="ShowEmbedDialogButton">
            <ShareAltOutlinedIcon /> Embed Elsewhere
          </PlainButton>
        </Menu.Item>
      )}
      <Menu.Item>
        <PlainButton
          onClick={() => props.copyToClipboard(props.query)}
          data-test="CopyToClipboard">
          <svg height="1em" version="1.1" viewBox="0 0 512 512" width="1em" ><g><g><path d="M160,160h192c-1.7-20-9.7-35.2-27.9-40.1c-0.4-0.1-0.9-0.3-1.3-0.4c-12-3.4-20.8-7.5-20.8-20.7V78.2    c0-25.5-20.5-46.3-46-46.3c-25.5,0-46,20.7-46,46.3v20.6c0,13.1-8.8,17.2-20.8,20.6c-0.4,0.1-0.9,0.4-1.4,0.5    C169.6,124.8,161.9,140,160,160z M256,64.4c7.6,0,13.8,6.2,13.8,13.8c0,7.7-6.2,13.8-13.8,13.8c-7.6,0-13.8-6.2-13.8-13.8    C242.2,70.6,248.4,64.4,256,64.4z"/><path d="M404.6,63H331v14.5c0,10.6,8.7,18.5,19,18.5h37.2c6.7,0,12.1,5.7,12.4,12.5l0.1,327.2c-0.3,6.4-5.3,11.6-11.5,12.1    l-264.4,0.1c-6.2-0.5-11.1-5.7-11.5-12.1l-0.1-327.3c0.3-6.8,5.9-12.5,12.5-12.5H162c10.3,0,19-7.9,19-18.5V63h-73.6    C92.3,63,80,76.1,80,91.6V452c0,15.5,12.3,28,27.4,28H256h148.6c15.1,0,27.4-12.5,27.4-28V91.6C432,76.1,419.7,63,404.6,63z"/></g><rect height="16" width="112" x="144" y="192"/><rect height="16" width="160" x="144" y="288"/><rect height="16" width="129" x="144" y="384"/><rect height="16" width="176" x="144" y="336"/><rect height="16" width="208" x="144" y="240"/></g></svg>
          Copy to clipboard
        </PlainButton>
      </Menu.Item>
      <Menu.Item>
        <QueryResultsLink
          fileType="csv"
          disabled={props.queryExecuting || !props.queryResult.getData || !props.queryResult.getData()}
          query={props.query}
          queryResult={props.queryResult}
          embed={props.embed}
          apiKey={props.apiKey}>
          <FileOutlinedIcon /> Download as CSV File
        </QueryResultsLink>
      </Menu.Item>
      <Menu.Item>
        <QueryResultsLink
          fileType="tsv"
          disabled={props.queryExecuting || !props.queryResult.getData || !props.queryResult.getData()}
          query={props.query}
          queryResult={props.queryResult}
          embed={props.embed}
          apiKey={props.apiKey}>
          <FileOutlinedIcon /> Download as TSV File
        </QueryResultsLink>
      </Menu.Item>
      <Menu.Item>
        <QueryResultsLink
          fileType="xlsx"
          disabled={props.queryExecuting || !props.queryResult.getData || !props.queryResult.getData()}
          query={props.query}
          queryResult={props.queryResult}
          embed={props.embed}
          apiKey={props.apiKey}>
          <FileExcelOutlinedIcon /> Download as Excel File
        </QueryResultsLink>
      </Menu.Item>
    </Menu>
  );

  return (
    <Dropdown trigger={["click"]} overlay={menu} overlayClassName="query-control-dropdown-overlay">
      <Button data-test="QueryControlDropdownButton">
        <EllipsisOutlinedIcon rotate={90} />
      </Button>
    </Dropdown>
  );
}

QueryControlDropdown.propTypes = {
  query: PropTypes.object.isRequired, // eslint-disable-line react/forbid-prop-types
  queryResult: PropTypes.object, // eslint-disable-line react/forbid-prop-types
  queryExecuting: PropTypes.bool.isRequired,
  showEmbedDialog: PropTypes.func.isRequired,
  copyToClipboard: PropTypes.func.isRequired,
  embed: PropTypes.bool,
  apiKey: PropTypes.string,
  selectedTab: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  openAddToDashboardForm: PropTypes.func.isRequired,
};

QueryControlDropdown.defaultProps = {
  queryResult: {},
  embed: false,
  apiKey: "",
  selectedTab: "",
};
