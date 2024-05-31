/*
 Navicat Premium Data Transfer

 Source Server         : sql3
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 04/01/2021 21:14:24
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for data
-- ----------------------------
DROP TABLE IF EXISTS "data";
CREATE TABLE "data" (
  "id" INTEGER NOT NULL,
  "name" TEXT NOT NULL,
  "c_na" TEXT NOT NULL,
  "pub_time" TEXT NOT NULL,
  "price" text NOT NULL,
  "score" TEXT NOT NULL,
  "comment_num" text NOT NULL,
  PRIMARY KEY ("id")
);

PRAGMA foreign_keys = true;
