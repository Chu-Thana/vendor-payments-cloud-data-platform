TRUNCATE TABLE landing.vendor_payments_streaming_events;

COPY landing.vendor_payments_streaming_events
FROM 's3://vendor-payments-data-platform-thana/data-platform/vendor-payments/streaming/curated/vendor_payments_streaming_events.csv'
IAM_ROLE default
FORMAT AS CSV
IGNOREHEADER 1
QUOTE AS '"'
REGION 'ap-southeast-1'
ACCEPTINVCHARS
TRUNCATECOLUMNS;