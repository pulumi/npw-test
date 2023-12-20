import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("my-bucket", {
    // Configure S3 bucket settings here.
});