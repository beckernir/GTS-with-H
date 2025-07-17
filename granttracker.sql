-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 17, 2025 at 04:03 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `granttracker`
--

-- --------------------------------------------------------

--
-- Table structure for table `ai_engine_aimodelstatus`
--

CREATE TABLE `ai_engine_aimodelstatus` (
  `id` bigint(20) NOT NULL,
  `component` varchar(50) NOT NULL,
  `status` varchar(20) NOT NULL,
  `progress` int(10) UNSIGNED NOT NULL CHECK (`progress` >= 0),
  `accuracy` double NOT NULL,
  `feature_importances` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`feature_importances`)),
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ai_engine_aimodelstatus`
--

INSERT INTO `ai_engine_aimodelstatus` (`id`, `component`, `status`, `progress`, `accuracy`, `feature_importances`, `updated_at`) VALUES
(1, 'prediction', 'active', 100, 4945625000000, '{\"requested_amount\": 1.0}', '2025-07-15 17:41:09.463576'),
(2, 'allocation', 'active', 100, 0, '{}', '2025-07-14 13:51:16.327943');

-- --------------------------------------------------------

--
-- Table structure for table `ai_engine_ai_performance_metrics`
--

CREATE TABLE `ai_engine_ai_performance_metrics` (
  `id` bigint(20) NOT NULL,
  `metric_id` char(32) NOT NULL,
  `metric_type` varchar(30) NOT NULL,
  `metric_name` varchar(100) NOT NULL,
  `metric_value` decimal(10,4) NOT NULL,
  `target_value` decimal(10,4) NOT NULL,
  `threshold_value` decimal(10,4) NOT NULL,
  `measurement_date` date NOT NULL,
  `measurement_period` varchar(50) NOT NULL,
  `is_above_target` tinyint(1) NOT NULL,
  `is_above_threshold` tinyint(1) NOT NULL,
  `trend_direction` varchar(10) NOT NULL,
  `metadata` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`metadata`)),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ai_engine_allocation_algorithm`
--

CREATE TABLE `ai_engine_allocation_algorithm` (
  `id` bigint(20) NOT NULL,
  `algorithm_id` char(32) NOT NULL,
  `algorithm_name` varchar(100) NOT NULL,
  `algorithm_type` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `configuration` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`configuration`)),
  `version` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  `accuracy_score` decimal(5,2) NOT NULL,
  `last_updated` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ai_engine_allocation_factor`
--

CREATE TABLE `ai_engine_allocation_factor` (
  `id` bigint(20) NOT NULL,
  `factor_id` char(32) NOT NULL,
  `factor_name` varchar(100) NOT NULL,
  `factor_category` varchar(20) NOT NULL,
  `factor_type` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `weight` decimal(5,2) NOT NULL,
  `min_value` decimal(10,2) NOT NULL,
  `max_value` decimal(10,2) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_required` tinyint(1) NOT NULL,
  `auto_calculate` tinyint(1) NOT NULL,
  `calculation_formula` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ai_engine_allocation_run`
--

CREATE TABLE `ai_engine_allocation_run` (
  `id` bigint(20) NOT NULL,
  `run_id` char(32) NOT NULL,
  `run_name` varchar(200) NOT NULL,
  `total_proposals` int(10) UNSIGNED NOT NULL CHECK (`total_proposals` >= 0),
  `total_budget_available` decimal(15,2) NOT NULL,
  `total_allocated` decimal(15,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `end_time` datetime(6) DEFAULT NULL,
  `duration_seconds` int(10) UNSIGNED NOT NULL CHECK (`duration_seconds` >= 0),
  `configuration` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`configuration`)),
  `results_summary` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`results_summary`)),
  `error_message` longtext DEFAULT NULL,
  `error_details` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`error_details`)),
  `created_at` datetime(6) NOT NULL,
  `algorithm_id` bigint(20) NOT NULL,
  `created_by_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ai_engine_optimization_recommendation`
--

CREATE TABLE `ai_engine_optimization_recommendation` (
  `id` bigint(20) NOT NULL,
  `recommendation_id` char(32) NOT NULL,
  `recommendation_type` varchar(30) NOT NULL,
  `priority` varchar(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `rationale` longtext NOT NULL,
  `expected_impact` longtext NOT NULL,
  `impact_score` decimal(5,2) NOT NULL,
  `implementation_steps` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`implementation_steps`)),
  `estimated_cost` decimal(12,2) NOT NULL,
  `estimated_duration_days` int(10) UNSIGNED NOT NULL CHECK (`estimated_duration_days` >= 0),
  `is_implemented` tinyint(1) NOT NULL,
  `implementation_date` datetime(6) DEFAULT NULL,
  `implementation_notes` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL,
  `implemented_by_id` bigint(20) DEFAULT NULL,
  `proposal_id` bigint(20) DEFAULT NULL,
  `school_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ai_engine_proposalanomaly`
--

CREATE TABLE `ai_engine_proposalanomaly` (
  `id` bigint(20) NOT NULL,
  `anomaly_type` varchar(50) NOT NULL,
  `score` double NOT NULL,
  `detected_at` datetime(6) NOT NULL,
  `proposal_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ai_engine_proposalanomaly`
--

INSERT INTO `ai_engine_proposalanomaly` (`id`, `anomaly_type`, `score`, `detected_at`, `proposal_id`) VALUES
(1, 'score', 1, '2025-07-01 10:33:52.426018', 17),
(2, 'score', 1, '2025-07-01 10:33:52.435875', 16),
(3, 'score', 1, '2025-07-01 10:33:52.450366', 15),
(4, 'score', 1, '2025-07-01 10:33:52.460047', 14),
(5, 'score', 1, '2025-07-01 10:33:52.468984', 13),
(6, 'score', 1, '2025-07-01 10:33:52.478056', 12),
(7, 'score', 1, '2025-07-01 10:33:52.490055', 11),
(8, 'score', 1, '2025-07-01 10:33:52.500688', 10),
(9, 'score', 1, '2025-07-01 10:33:52.509715', 9),
(10, 'score', 1, '2025-07-01 10:33:52.520209', 8),
(11, 'score', 1, '2025-07-01 10:33:52.527609', 7),
(12, 'score', 1, '2025-07-01 10:33:52.542530', 5),
(13, 'score', 1, '2025-07-01 10:37:24.287172', 17),
(14, 'score', 1, '2025-07-01 10:37:24.295307', 16),
(15, 'score', 1, '2025-07-01 10:37:24.302420', 15),
(16, 'score', 1, '2025-07-01 10:37:24.311412', 14),
(17, 'score', 1, '2025-07-01 10:37:24.319000', 13),
(18, 'score', 1, '2025-07-01 10:37:24.326999', 12),
(19, 'score', 1, '2025-07-01 10:37:24.333999', 11),
(20, 'score', 1, '2025-07-01 10:37:24.340157', 10),
(21, 'score', 1, '2025-07-01 10:37:24.346519', 9),
(22, 'score', 1, '2025-07-01 10:37:24.352465', 8),
(23, 'score', 1, '2025-07-01 10:37:24.359471', 7),
(24, 'score', 1, '2025-07-01 10:37:24.369543', 5),
(25, 'score', 1, '2025-07-01 10:37:38.907560', 17),
(26, 'score', 1, '2025-07-01 10:37:38.916031', 16),
(27, 'score', 1, '2025-07-01 10:37:38.922972', 15),
(28, 'score', 1, '2025-07-01 10:37:38.930972', 14),
(29, 'score', 1, '2025-07-01 10:37:38.936990', 13),
(30, 'score', 1, '2025-07-01 10:37:38.943118', 12),
(31, 'score', 1, '2025-07-01 10:37:38.951336', 11),
(32, 'score', 1, '2025-07-01 10:37:38.957333', 10),
(33, 'score', 1, '2025-07-01 10:37:38.963780', 9),
(34, 'score', 1, '2025-07-01 10:37:38.970400', 8),
(35, 'score', 1, '2025-07-01 10:37:38.975395', 7),
(36, 'score', 1, '2025-07-01 10:37:38.987403', 5),
(37, 'score', 1, '2025-07-01 10:48:28.840527', 17),
(38, 'score', 1, '2025-07-01 10:48:28.849503', 16),
(39, 'score', 1, '2025-07-01 10:48:28.855420', 15),
(40, 'score', 1, '2025-07-01 10:48:28.863683', 14),
(41, 'score', 1, '2025-07-01 10:48:28.869940', 13),
(42, 'score', 1, '2025-07-01 10:48:28.875340', 12),
(43, 'score', 1, '2025-07-01 10:48:28.884531', 11),
(44, 'score', 1, '2025-07-01 10:48:28.889680', 10),
(45, 'score', 1, '2025-07-01 10:48:28.917585', 9),
(46, 'score', 1, '2025-07-01 10:48:28.923769', 8),
(47, 'score', 1, '2025-07-01 10:48:28.933809', 7),
(48, 'score', 1, '2025-07-01 10:48:28.947600', 5),
(49, 'score', 1, '2025-07-01 10:51:56.435757', 17),
(50, 'score', 1, '2025-07-01 10:51:56.444670', 16),
(51, 'score', 1, '2025-07-01 10:51:56.451597', 15),
(52, 'score', 1, '2025-07-01 10:51:56.458579', 14),
(53, 'score', 1, '2025-07-01 10:51:56.464630', 13),
(54, 'score', 1, '2025-07-01 10:51:56.470872', 12),
(55, 'score', 1, '2025-07-01 10:51:56.477873', 11),
(56, 'score', 1, '2025-07-01 10:51:56.484873', 10),
(57, 'score', 1, '2025-07-01 10:51:56.494220', 9),
(58, 'score', 1, '2025-07-01 10:51:56.499373', 8),
(59, 'score', 1, '2025-07-01 10:51:56.505373', 7),
(60, 'score', 1, '2025-07-01 10:51:56.516380', 5),
(61, 'score', 1, '2025-07-01 10:52:02.649564', 17),
(62, 'score', 1, '2025-07-01 10:52:02.657566', 16),
(63, 'score', 1, '2025-07-01 10:52:02.665565', 15),
(64, 'score', 1, '2025-07-01 10:52:02.674565', 14),
(65, 'score', 1, '2025-07-01 10:52:02.681564', 13),
(66, 'score', 1, '2025-07-01 10:52:02.692567', 12),
(67, 'score', 1, '2025-07-01 10:52:02.699564', 11),
(68, 'score', 1, '2025-07-01 10:52:02.709566', 10),
(69, 'score', 1, '2025-07-01 10:52:02.716565', 9),
(70, 'score', 1, '2025-07-01 10:52:02.724565', 8),
(71, 'score', 1, '2025-07-01 10:52:02.731565', 7),
(72, 'score', 1, '2025-07-01 10:52:02.744569', 5),
(73, 'score', 1, '2025-07-01 10:52:04.895374', 17),
(74, 'score', 1, '2025-07-01 10:52:04.907081', 16),
(75, 'score', 1, '2025-07-01 10:52:04.915079', 15),
(76, 'score', 1, '2025-07-01 10:52:04.924080', 14),
(77, 'score', 1, '2025-07-01 10:52:04.931080', 13),
(78, 'score', 1, '2025-07-01 10:52:04.940086', 12),
(79, 'score', 1, '2025-07-01 10:52:04.947086', 11),
(80, 'score', 1, '2025-07-01 10:52:04.956368', 10),
(81, 'score', 1, '2025-07-01 10:52:04.963368', 9),
(82, 'score', 1, '2025-07-01 10:52:04.971368', 8),
(83, 'score', 1, '2025-07-01 10:52:04.978368', 7),
(84, 'score', 1, '2025-07-01 10:52:04.991368', 5),
(85, 'score', 1, '2025-07-01 10:52:06.394651', 17),
(86, 'score', 1, '2025-07-01 10:52:06.403650', 16),
(87, 'score', 1, '2025-07-01 10:52:06.410673', 15),
(88, 'score', 1, '2025-07-01 10:52:06.419657', 14),
(89, 'score', 1, '2025-07-01 10:52:06.426060', 13),
(90, 'score', 1, '2025-07-01 10:52:06.434669', 12),
(91, 'score', 1, '2025-07-01 10:52:06.440667', 11),
(92, 'score', 1, '2025-07-01 10:52:06.448641', 10),
(93, 'score', 1, '2025-07-01 10:52:06.454699', 9),
(94, 'score', 1, '2025-07-01 10:52:06.460706', 8),
(95, 'score', 1, '2025-07-01 10:52:06.467686', 7),
(96, 'score', 1, '2025-07-01 10:52:06.479666', 5),
(97, 'score', 1, '2025-07-01 10:52:20.640327', 17),
(98, 'score', 1, '2025-07-01 10:52:20.647273', 16),
(99, 'score', 1, '2025-07-01 10:52:20.655273', 15),
(100, 'score', 1, '2025-07-01 10:52:20.661581', 14),
(101, 'score', 1, '2025-07-01 10:52:20.666244', 13),
(102, 'score', 1, '2025-07-01 10:52:20.674230', 12),
(103, 'score', 1, '2025-07-01 10:52:20.682204', 11),
(104, 'score', 1, '2025-07-01 10:52:20.690105', 10),
(105, 'score', 1, '2025-07-01 10:52:20.696124', 9),
(106, 'score', 1, '2025-07-01 10:52:20.701218', 8),
(107, 'score', 1, '2025-07-01 10:52:20.708219', 7),
(108, 'score', 1, '2025-07-01 10:52:20.719167', 5),
(109, 'score', 1, '2025-07-01 10:52:23.498561', 17),
(110, 'score', 1, '2025-07-01 10:52:23.506562', 16),
(111, 'score', 1, '2025-07-01 10:52:23.512560', 15),
(112, 'score', 1, '2025-07-01 10:52:23.519302', 14),
(113, 'score', 1, '2025-07-01 10:52:23.525300', 13),
(114, 'score', 1, '2025-07-01 10:52:23.531327', 12),
(115, 'score', 1, '2025-07-01 10:52:23.537330', 11),
(116, 'score', 1, '2025-07-01 10:52:23.543347', 10),
(117, 'score', 1, '2025-07-01 10:52:23.548740', 9),
(118, 'score', 1, '2025-07-01 10:52:23.555235', 8),
(119, 'score', 1, '2025-07-01 10:52:23.560708', 7),
(120, 'score', 1, '2025-07-01 10:52:23.572686', 5),
(121, 'score', 1, '2025-07-01 10:54:06.920103', 17),
(122, 'score', 1, '2025-07-01 10:54:06.929105', 16),
(123, 'score', 1, '2025-07-01 10:54:06.940126', 15),
(124, 'score', 1, '2025-07-01 10:54:06.948104', 14),
(125, 'score', 1, '2025-07-01 10:54:06.960108', 13),
(126, 'score', 1, '2025-07-01 10:54:06.971103', 12),
(127, 'score', 1, '2025-07-01 10:54:06.979103', 11),
(128, 'score', 1, '2025-07-01 10:54:06.988103', 10),
(129, 'score', 1, '2025-07-01 10:54:07.003113', 9),
(130, 'score', 1, '2025-07-01 10:54:07.011639', 8),
(131, 'score', 1, '2025-07-01 10:54:07.021639', 7),
(132, 'score', 1, '2025-07-01 10:54:07.038639', 5);

-- --------------------------------------------------------

--
-- Table structure for table `ai_engine_proposalprediction`
--

CREATE TABLE `ai_engine_proposalprediction` (
  `id` bigint(20) NOT NULL,
  `score` double NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `proposal_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ai_engine_proposalprediction`
--

INSERT INTO `ai_engine_proposalprediction` (`id`, `score`, `updated_at`, `proposal_id`) VALUES
(1, 1, '2025-07-14 13:51:12.903349', 17),
(2, 1, '2025-07-14 13:51:12.915906', 16),
(3, 1, '2025-07-14 13:51:12.928923', 15),
(4, 1, '2025-07-14 13:51:12.940474', 14),
(5, 1, '2025-07-14 13:51:12.950503', 13),
(6, 1, '2025-07-14 13:51:12.962591', 12),
(7, 1, '2025-07-14 13:51:12.973709', 11),
(8, 1, '2025-07-14 13:51:12.984725', 10),
(9, 1, '2025-07-14 13:51:12.996862', 9),
(10, 1, '2025-07-14 13:51:13.008358', 8),
(11, 1, '2025-07-14 13:51:13.018888', 7),
(12, 0.88, '2025-07-14 13:51:13.031476', 6),
(13, 1, '2025-07-14 13:51:13.043548', 5),
(14, 0.88, '2025-07-14 13:51:13.054648', 4),
(15, 0.37, '2025-07-14 13:51:13.065671', 3),
(16, 0.37, '2025-07-14 13:51:13.077324', 2);

-- --------------------------------------------------------

--
-- Table structure for table `ai_engine_proposal_allocation_score`
--

CREATE TABLE `ai_engine_proposal_allocation_score` (
  `id` bigint(20) NOT NULL,
  `score_id` char(32) NOT NULL,
  `total_score` decimal(5,2) NOT NULL,
  `rank` int(10) UNSIGNED NOT NULL CHECK (`rank` >= 0),
  `factor_scores` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`factor_scores`)),
  `recommended_amount` decimal(12,2) NOT NULL,
  `allocation_percentage` decimal(5,2) NOT NULL,
  `is_allocated` tinyint(1) NOT NULL,
  `allocated_amount` decimal(12,2) NOT NULL,
  `allocation_date` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `allocation_run_id` bigint(20) NOT NULL,
  `proposal_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ai_engine_recommendationaction`
--

CREATE TABLE `ai_engine_recommendationaction` (
  `id` bigint(20) NOT NULL,
  `proposal_title` varchar(255) NOT NULL,
  `action` varchar(20) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ai_engine_recommendationaction`
--

INSERT INTO `ai_engine_recommendationaction` (`id`, `proposal_title`, `action`, `timestamp`, `user_id`) VALUES
(1, 'Grant Proposal Northern 3', 'review', '2025-07-01 10:09:32.123132', 6),
(2, 'Grant Proposal Southern 3', 'accept', '2025-07-01 10:33:00.903194', 6),
(3, 'Grant Proposal Northern 2', 'review', '2025-07-02 11:52:55.188878', 6),
(4, 'Grant Proposal Western 3', 'accept', '2025-07-02 11:52:57.944127', 6);

-- --------------------------------------------------------

--
-- Table structure for table `ai_engine_risk_assessment`
--

CREATE TABLE `ai_engine_risk_assessment` (
  `id` bigint(20) NOT NULL,
  `risk_id` char(32) NOT NULL,
  `risk_name` varchar(200) NOT NULL,
  `risk_category` varchar(20) NOT NULL,
  `risk_level` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `risk_factors` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`risk_factors`)),
  `risk_score` decimal(5,2) NOT NULL,
  `mitigation_strategies` longtext DEFAULT NULL,
  `monitoring_requirements` longtext DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_resolved` tinyint(1) NOT NULL,
  `resolution_date` datetime(6) DEFAULT NULL,
  `resolution_notes` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL,
  `proposal_id` bigint(20) DEFAULT NULL,
  `resolved_by_id` bigint(20) DEFAULT NULL,
  `school_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add User', 6, 'add_user'),
(22, 'Can change User', 6, 'change_user'),
(23, 'Can delete User', 6, 'delete_user'),
(24, 'Can view User', 6, 'view_user'),
(25, 'Can add District', 7, 'add_district'),
(26, 'Can change District', 7, 'change_district'),
(27, 'Can delete District', 7, 'delete_district'),
(28, 'Can view District', 7, 'view_district'),
(29, 'Can add School', 8, 'add_school'),
(30, 'Can change School', 8, 'change_school'),
(31, 'Can delete School', 8, 'delete_school'),
(32, 'Can view School', 8, 'view_school'),
(33, 'Can add System Configuration', 9, 'add_systemconfiguration'),
(34, 'Can change System Configuration', 9, 'change_systemconfiguration'),
(35, 'Can delete System Configuration', 9, 'delete_systemconfiguration'),
(36, 'Can view System Configuration', 9, 'view_systemconfiguration'),
(37, 'Can add School User Assignment', 10, 'add_schooluser'),
(38, 'Can change School User Assignment', 10, 'change_schooluser'),
(39, 'Can delete School User Assignment', 10, 'delete_schooluser'),
(40, 'Can view School User Assignment', 10, 'view_schooluser'),
(41, 'Can add Grant Category', 11, 'add_grantcategory'),
(42, 'Can change Grant Category', 11, 'change_grantcategory'),
(43, 'Can delete Grant Category', 11, 'delete_grantcategory'),
(44, 'Can view Grant Category', 11, 'view_grantcategory'),
(45, 'Can add Grant Proposal', 12, 'add_grantproposal'),
(46, 'Can change Grant Proposal', 12, 'change_grantproposal'),
(47, 'Can delete Grant Proposal', 12, 'delete_grantproposal'),
(48, 'Can view Grant Proposal', 12, 'view_grantproposal'),
(49, 'Can add Proposal Review', 13, 'add_proposalreview'),
(50, 'Can change Proposal Review', 13, 'change_proposalreview'),
(51, 'Can delete Proposal Review', 13, 'delete_proposalreview'),
(52, 'Can view Proposal Review', 13, 'view_proposalreview'),
(53, 'Can add Proposal Document', 14, 'add_proposaldocument'),
(54, 'Can change Proposal Document', 14, 'change_proposaldocument'),
(55, 'Can delete Proposal Document', 14, 'delete_proposaldocument'),
(56, 'Can view Proposal Document', 14, 'view_proposaldocument'),
(57, 'Can add Proposal Budget Item', 15, 'add_proposalbudget'),
(58, 'Can change Proposal Budget Item', 15, 'change_proposalbudget'),
(59, 'Can delete Proposal Budget Item', 15, 'delete_proposalbudget'),
(60, 'Can view Proposal Budget Item', 15, 'view_proposalbudget'),
(61, 'Can add Fund Allocation', 16, 'add_fundallocation'),
(62, 'Can change Fund Allocation', 16, 'change_fundallocation'),
(63, 'Can delete Fund Allocation', 16, 'delete_fundallocation'),
(64, 'Can view Fund Allocation', 16, 'view_fundallocation'),
(65, 'Can add Budget Category', 17, 'add_budgetcategory'),
(66, 'Can change Budget Category', 17, 'change_budgetcategory'),
(67, 'Can delete Budget Category', 17, 'delete_budgetcategory'),
(68, 'Can view Budget Category', 17, 'view_budgetcategory'),
(69, 'Can add Budget Line Item', 18, 'add_budgetlineitem'),
(70, 'Can change Budget Line Item', 18, 'change_budgetlineitem'),
(71, 'Can delete Budget Line Item', 18, 'delete_budgetlineitem'),
(72, 'Can view Budget Line Item', 18, 'view_budgetlineitem'),
(73, 'Can add Budget Period', 19, 'add_budgetperiod'),
(74, 'Can change Budget Period', 19, 'change_budgetperiod'),
(75, 'Can delete Budget Period', 19, 'delete_budgetperiod'),
(76, 'Can view Budget Period', 19, 'view_budgetperiod'),
(77, 'Can add Budget Report', 20, 'add_budgetreport'),
(78, 'Can change Budget Report', 20, 'change_budgetreport'),
(79, 'Can delete Budget Report', 20, 'delete_budgetreport'),
(80, 'Can view Budget Report', 20, 'view_budgetreport'),
(81, 'Can add Budget Transfer', 21, 'add_budgettransfer'),
(82, 'Can change Budget Transfer', 21, 'change_budgettransfer'),
(83, 'Can delete Budget Transfer', 21, 'delete_budgettransfer'),
(84, 'Can view Budget Transfer', 21, 'view_budgettransfer'),
(85, 'Can add Expenditure', 22, 'add_expenditure'),
(86, 'Can change Expenditure', 22, 'change_expenditure'),
(87, 'Can delete Expenditure', 22, 'delete_expenditure'),
(88, 'Can view Expenditure', 22, 'view_expenditure'),
(89, 'Can add School Budget', 23, 'add_schoolbudget'),
(90, 'Can change School Budget', 23, 'change_schoolbudget'),
(91, 'Can delete School Budget', 23, 'delete_schoolbudget'),
(92, 'Can view School Budget', 23, 'view_schoolbudget'),
(93, 'Can add Dashboard', 24, 'add_dashboard'),
(94, 'Can change Dashboard', 24, 'change_dashboard'),
(95, 'Can delete Dashboard', 24, 'delete_dashboard'),
(96, 'Can view Dashboard', 24, 'view_dashboard'),
(97, 'Can add KPI', 25, 'add_kpi'),
(98, 'Can change KPI', 25, 'change_kpi'),
(99, 'Can delete KPI', 25, 'delete_kpi'),
(100, 'Can view KPI', 25, 'view_kpi'),
(101, 'Can add Report', 26, 'add_report'),
(102, 'Can change Report', 26, 'change_report'),
(103, 'Can delete Report', 26, 'delete_report'),
(104, 'Can view Report', 26, 'view_report'),
(105, 'Can add Report Schedule', 27, 'add_reportschedule'),
(106, 'Can change Report Schedule', 27, 'change_reportschedule'),
(107, 'Can delete Report Schedule', 27, 'delete_reportschedule'),
(108, 'Can view Report Schedule', 27, 'view_reportschedule'),
(109, 'Can add Data Export', 28, 'add_dataexport'),
(110, 'Can change Data Export', 28, 'change_dataexport'),
(111, 'Can delete Data Export', 28, 'delete_dataexport'),
(112, 'Can view Data Export', 28, 'view_dataexport'),
(113, 'Can add Dashboard Widget', 29, 'add_dashboardwidget'),
(114, 'Can change Dashboard Widget', 29, 'change_dashboardwidget'),
(115, 'Can delete Dashboard Widget', 29, 'delete_dashboardwidget'),
(116, 'Can view Dashboard Widget', 29, 'view_dashboardwidget'),
(117, 'Can add Analytics Event', 30, 'add_analyticsevent'),
(118, 'Can change Analytics Event', 30, 'change_analyticsevent'),
(119, 'Can delete Analytics Event', 30, 'delete_analyticsevent'),
(120, 'Can view Analytics Event', 30, 'view_analyticsevent'),
(121, 'Can add KPI Value', 31, 'add_kpivalue'),
(122, 'Can change KPI Value', 31, 'change_kpivalue'),
(123, 'Can delete KPI Value', 31, 'delete_kpivalue'),
(124, 'Can view KPI Value', 31, 'view_kpivalue'),
(125, 'Can add Course Module', 32, 'add_coursemodule'),
(126, 'Can change Course Module', 32, 'change_coursemodule'),
(127, 'Can delete Course Module', 32, 'delete_coursemodule'),
(128, 'Can view Course Module', 32, 'view_coursemodule'),
(129, 'Can add Training Category', 33, 'add_trainingcategory'),
(130, 'Can change Training Category', 33, 'change_trainingcategory'),
(131, 'Can delete Training Category', 33, 'delete_trainingcategory'),
(132, 'Can view Training Category', 33, 'view_trainingcategory'),
(133, 'Can add Training Course', 34, 'add_trainingcourse'),
(134, 'Can change Training Course', 34, 'change_trainingcourse'),
(135, 'Can delete Training Course', 34, 'delete_trainingcourse'),
(136, 'Can view Training Course', 34, 'view_trainingcourse'),
(137, 'Can add Training Session', 35, 'add_trainingsession'),
(138, 'Can change Training Session', 35, 'change_trainingsession'),
(139, 'Can delete Training Session', 35, 'delete_trainingsession'),
(140, 'Can view Training Session', 35, 'view_trainingsession'),
(141, 'Can add Training Enrollment', 36, 'add_trainingenrollment'),
(142, 'Can change Training Enrollment', 36, 'change_trainingenrollment'),
(143, 'Can delete Training Enrollment', 36, 'delete_trainingenrollment'),
(144, 'Can view Training Enrollment', 36, 'view_trainingenrollment'),
(145, 'Can add Training Certificate', 37, 'add_trainingcertificate'),
(146, 'Can change Training Certificate', 37, 'change_trainingcertificate'),
(147, 'Can delete Training Certificate', 37, 'delete_trainingcertificate'),
(148, 'Can view Training Certificate', 37, 'view_trainingcertificate'),
(149, 'Can add Training Assessment', 38, 'add_trainingassessment'),
(150, 'Can change Training Assessment', 38, 'change_trainingassessment'),
(151, 'Can delete Training Assessment', 38, 'delete_trainingassessment'),
(152, 'Can view Training Assessment', 38, 'view_trainingassessment'),
(153, 'Can add Assessment Result', 39, 'add_assessmentresult'),
(154, 'Can change Assessment Result', 39, 'change_assessmentresult'),
(155, 'Can delete Assessment Result', 39, 'delete_assessmentresult'),
(156, 'Can view Assessment Result', 39, 'view_assessmentresult'),
(157, 'Can add Module Progress', 40, 'add_moduleprogress'),
(158, 'Can change Module Progress', 40, 'change_moduleprogress'),
(159, 'Can delete Module Progress', 40, 'delete_moduleprogress'),
(160, 'Can view Module Progress', 40, 'view_moduleprogress'),
(161, 'Can add Announcement', 41, 'add_announcement'),
(162, 'Can change Announcement', 41, 'change_announcement'),
(163, 'Can delete Announcement', 41, 'delete_announcement'),
(164, 'Can view Announcement', 41, 'view_announcement'),
(165, 'Can add Community Event', 42, 'add_communityevent'),
(166, 'Can change Community Event', 42, 'change_communityevent'),
(167, 'Can delete Community Event', 42, 'delete_communityevent'),
(168, 'Can view Community Event', 42, 'view_communityevent'),
(169, 'Can add Community Forum', 43, 'add_communityforum'),
(170, 'Can change Community Forum', 43, 'change_communityforum'),
(171, 'Can delete Community Forum', 43, 'delete_communityforum'),
(172, 'Can view Community Forum', 43, 'view_communityforum'),
(173, 'Can add Community Message', 44, 'add_communitymessage'),
(174, 'Can change Community Message', 44, 'change_communitymessage'),
(175, 'Can delete Community Message', 44, 'delete_communitymessage'),
(176, 'Can view Community Message', 44, 'view_communitymessage'),
(177, 'Can add Feedback', 45, 'add_feedback'),
(178, 'Can change Feedback', 45, 'change_feedback'),
(179, 'Can delete Feedback', 45, 'delete_feedback'),
(180, 'Can view Feedback', 45, 'view_feedback'),
(181, 'Can add Forum Post', 46, 'add_forumpost'),
(182, 'Can change Forum Post', 46, 'change_forumpost'),
(183, 'Can delete Forum Post', 46, 'delete_forumpost'),
(184, 'Can view Forum Post', 46, 'view_forumpost'),
(185, 'Can add Forum Topic', 47, 'add_forumtopic'),
(186, 'Can change Forum Topic', 47, 'change_forumtopic'),
(187, 'Can delete Forum Topic', 47, 'delete_forumtopic'),
(188, 'Can view Forum Topic', 47, 'view_forumtopic'),
(189, 'Can add AI Performance Metric', 48, 'add_aiperformancemetrics'),
(190, 'Can change AI Performance Metric', 48, 'change_aiperformancemetrics'),
(191, 'Can delete AI Performance Metric', 48, 'delete_aiperformancemetrics'),
(192, 'Can view AI Performance Metric', 48, 'view_aiperformancemetrics'),
(193, 'Can add Allocation Algorithm', 49, 'add_allocationalgorithm'),
(194, 'Can change Allocation Algorithm', 49, 'change_allocationalgorithm'),
(195, 'Can delete Allocation Algorithm', 49, 'delete_allocationalgorithm'),
(196, 'Can view Allocation Algorithm', 49, 'view_allocationalgorithm'),
(197, 'Can add Allocation Factor', 50, 'add_allocationfactor'),
(198, 'Can change Allocation Factor', 50, 'change_allocationfactor'),
(199, 'Can delete Allocation Factor', 50, 'delete_allocationfactor'),
(200, 'Can view Allocation Factor', 50, 'view_allocationfactor'),
(201, 'Can add Allocation Run', 51, 'add_allocationrun'),
(202, 'Can change Allocation Run', 51, 'change_allocationrun'),
(203, 'Can delete Allocation Run', 51, 'delete_allocationrun'),
(204, 'Can view Allocation Run', 51, 'view_allocationrun'),
(205, 'Can add Optimization Recommendation', 52, 'add_optimizationrecommendation'),
(206, 'Can change Optimization Recommendation', 52, 'change_optimizationrecommendation'),
(207, 'Can delete Optimization Recommendation', 52, 'delete_optimizationrecommendation'),
(208, 'Can view Optimization Recommendation', 52, 'view_optimizationrecommendation'),
(209, 'Can add Proposal Allocation Score', 53, 'add_proposalallocationscore'),
(210, 'Can change Proposal Allocation Score', 53, 'change_proposalallocationscore'),
(211, 'Can delete Proposal Allocation Score', 53, 'delete_proposalallocationscore'),
(212, 'Can view Proposal Allocation Score', 53, 'view_proposalallocationscore'),
(213, 'Can add Risk Assessment', 54, 'add_riskassessment'),
(214, 'Can change Risk Assessment', 54, 'change_riskassessment'),
(215, 'Can delete Risk Assessment', 54, 'delete_riskassessment'),
(216, 'Can view Risk Assessment', 54, 'view_riskassessment'),
(217, 'Can add audit log', 55, 'add_auditlog'),
(218, 'Can change audit log', 55, 'change_auditlog'),
(219, 'Can delete audit log', 55, 'delete_auditlog'),
(220, 'Can view audit log', 55, 'view_auditlog'),
(221, 'Can add recommendation action', 56, 'add_recommendationaction'),
(222, 'Can change recommendation action', 56, 'change_recommendationaction'),
(223, 'Can delete recommendation action', 56, 'delete_recommendationaction'),
(224, 'Can view recommendation action', 56, 'view_recommendationaction'),
(225, 'Can add ai model status', 57, 'add_aimodelstatus'),
(226, 'Can change ai model status', 57, 'change_aimodelstatus'),
(227, 'Can delete ai model status', 57, 'delete_aimodelstatus'),
(228, 'Can view ai model status', 57, 'view_aimodelstatus'),
(229, 'Can add proposal anomaly', 58, 'add_proposalanomaly'),
(230, 'Can change proposal anomaly', 58, 'change_proposalanomaly'),
(231, 'Can delete proposal anomaly', 58, 'delete_proposalanomaly'),
(232, 'Can view proposal anomaly', 58, 'view_proposalanomaly'),
(233, 'Can add proposal prediction', 59, 'add_proposalprediction'),
(234, 'Can change proposal prediction', 59, 'change_proposalprediction'),
(235, 'Can delete proposal prediction', 59, 'delete_proposalprediction'),
(236, 'Can view proposal prediction', 59, 'view_proposalprediction'),
(237, 'Can add tender status history', 60, 'add_tenderstatushistory'),
(238, 'Can change tender status history', 60, 'change_tenderstatushistory'),
(239, 'Can delete tender status history', 60, 'delete_tenderstatushistory'),
(240, 'Can view tender status history', 60, 'view_tenderstatushistory'),
(241, 'Can add tender', 61, 'add_tender'),
(242, 'Can change tender', 61, 'change_tender'),
(243, 'Can delete tender', 61, 'delete_tender'),
(244, 'Can view tender', 61, 'view_tender'),
(245, 'Can add tender document', 62, 'add_tenderdocument'),
(246, 'Can change tender document', 62, 'change_tenderdocument'),
(247, 'Can delete tender document', 62, 'delete_tenderdocument'),
(248, 'Can view tender document', 62, 'view_tenderdocument'),
(249, 'Can add bid', 63, 'add_bid'),
(250, 'Can change bid', 63, 'change_bid'),
(251, 'Can delete bid', 63, 'delete_bid'),
(252, 'Can view bid', 63, 'view_bid'),
(253, 'Can add REB Grant Budget', 64, 'add_rebgrantbudget'),
(254, 'Can change REB Grant Budget', 64, 'change_rebgrantbudget'),
(255, 'Can delete REB Grant Budget', 64, 'delete_rebgrantbudget'),
(256, 'Can view REB Grant Budget', 64, 'view_rebgrantbudget'),
(257, 'Can add Proposal Criterion', 65, 'add_proposalcriterion'),
(258, 'Can change Proposal Criterion', 65, 'change_proposalcriterion'),
(259, 'Can delete Proposal Criterion', 65, 'delete_proposalcriterion'),
(260, 'Can view Proposal Criterion', 65, 'view_proposalcriterion'),
(261, 'Can add Supplier Criterion', 66, 'add_suppliercriterion'),
(262, 'Can change Supplier Criterion', 66, 'change_suppliercriterion'),
(263, 'Can delete Supplier Criterion', 66, 'delete_suppliercriterion'),
(264, 'Can view Supplier Criterion', 66, 'view_suppliercriterion'),
(265, 'Can add supplier criterion response', 67, 'add_suppliercriterionresponse'),
(266, 'Can change supplier criterion response', 67, 'change_suppliercriterionresponse'),
(267, 'Can delete supplier criterion response', 67, 'delete_suppliercriterionresponse'),
(268, 'Can view supplier criterion response', 67, 'view_suppliercriterionresponse'),
(269, 'Can add proposal criterion response', 68, 'add_proposalcriterionresponse'),
(270, 'Can change proposal criterion response', 68, 'change_proposalcriterionresponse'),
(271, 'Can delete proposal criterion response', 68, 'delete_proposalcriterionresponse'),
(272, 'Can view proposal criterion response', 68, 'view_proposalcriterionresponse');

-- --------------------------------------------------------

--
-- Table structure for table `budget_budget_category`
--

CREATE TABLE `budget_budget_category` (
  `id` bigint(20) NOT NULL,
  `category_id` char(32) NOT NULL,
  `category_name` varchar(100) NOT NULL,
  `category_type` varchar(20) NOT NULL,
  `description` longtext DEFAULT NULL,
  `budget_limit` decimal(12,2) NOT NULL,
  `allocated_amount` decimal(12,2) NOT NULL,
  `spent_amount` decimal(12,2) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `requires_approval` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `budget_budget_category`
--

INSERT INTO `budget_budget_category` (`id`, `category_id`, `category_name`, `category_type`, `description`, `budget_limit`, `allocated_amount`, `spent_amount`, `is_active`, `requires_approval`, `created_at`, `updated_at`) VALUES
(1, 'e5133ea3c8744f698a79c90c43ea72a4', 'Instructional Materials', 'equipment', NULL, 2000000.00, 1500000.00, 500000.00, 1, 0, '2025-06-30 16:16:04.979104', '2025-06-30 16:16:04.979104'),
(2, '702e17f2005a4257a48b017780492865', 'Infrastructure', 'other', NULL, 0.00, 0.00, 0.00, 1, 0, '2025-07-01 11:02:28.445013', '2025-07-01 11:02:28.445013');

-- --------------------------------------------------------

--
-- Table structure for table `budget_budget_line_item`
--

CREATE TABLE `budget_budget_line_item` (
  `id` bigint(20) NOT NULL,
  `line_item_id` char(32) NOT NULL,
  `item_description` varchar(200) NOT NULL,
  `item_details` longtext DEFAULT NULL,
  `quantity` int(10) UNSIGNED NOT NULL CHECK (`quantity` >= 0),
  `unit_cost` decimal(10,2) NOT NULL,
  `total_cost` decimal(12,2) NOT NULL,
  `allocated_amount` decimal(12,2) NOT NULL,
  `spent_amount` decimal(12,2) NOT NULL,
  `committed_amount` decimal(12,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `planned_date` date NOT NULL,
  `completion_date` date DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `budget_category_id` bigint(20) NOT NULL,
  `created_by_id` bigint(20) NOT NULL,
  `related_proposal_id` bigint(20) DEFAULT NULL,
  `school_budget_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `budget_budget_line_item`
--

INSERT INTO `budget_budget_line_item` (`id`, `line_item_id`, `item_description`, `item_details`, `quantity`, `unit_cost`, `total_cost`, `allocated_amount`, `spent_amount`, `committed_amount`, `status`, `planned_date`, `completion_date`, `created_at`, `updated_at`, `budget_category_id`, `created_by_id`, `related_proposal_id`, `school_budget_id`) VALUES
(1, 'dc4546db474742a3b02b34fa1bdeca93', 'Books', NULL, 100, 10000.00, 1000000.00, 1000000.00, 200000.00, 0.00, 'planned', '2025-06-30', NULL, '2025-06-30 16:16:04.987110', '2025-06-30 16:16:04.987110', 1, 6, NULL, 3),
(2, '88b740d4573f4831afc29400f0ec9a14', 'Notebooks', NULL, 200, 5000.00, 1000000.00, 500000.00, 300000.00, 0.00, 'planned', '2025-06-30', NULL, '2025-06-30 16:16:04.991106', '2025-06-30 16:16:04.991106', 1, 6, NULL, 3),
(3, 'd96eccac080c4befb9d94a1db1ac51a2', 'Demo Item', NULL, 1, 40000.00, 40000.00, 40000.00, 25000.00, 0.00, 'planned', '2025-07-01', NULL, '2025-07-01 11:04:22.710310', '2025-07-01 11:04:22.710310', 1, 13, NULL, 5),
(5, '075ba67079194b8f85c613d3a2955ee6', 'Infra Demo', NULL, 1, 500000.00, 500000.00, 500000.00, 200000.00, 0.00, 'planned', '2025-07-01', NULL, '2025-07-01 11:11:59.573021', '2025-07-01 11:11:59.573021', 2, 13, NULL, 5);

-- --------------------------------------------------------

--
-- Table structure for table `budget_budget_period`
--

CREATE TABLE `budget_budget_period` (
  `id` bigint(20) NOT NULL,
  `period_id` char(32) NOT NULL,
  `period_name` varchar(100) NOT NULL,
  `period_type` varchar(20) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `total_budget_limit` decimal(15,2) NOT NULL,
  `allocated_budget` decimal(15,2) NOT NULL,
  `spent_budget` decimal(15,2) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_closed` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `budget_budget_period`
--

INSERT INTO `budget_budget_period` (`id`, `period_id`, `period_name`, `period_type`, `start_date`, `end_date`, `total_budget_limit`, `allocated_budget`, `spent_budget`, `is_active`, `is_closed`, `created_at`, `updated_at`, `created_by_id`) VALUES
(1, '12ef5227b694410394719ff6cf89c6f3', 'Business incubtion 2025', 'fiscal_year', '2025-06-30', '2026-06-30', 20000.00, 0.00, 0.00, 1, 0, '2025-06-30 15:07:11.396460', '2025-06-30 15:18:44.623856', 6),
(3, '9ed88e917b3f454c8674951735e37755', '2024-2025', 'fiscal_year', '2024-07-01', '2025-06-30', 10000000.00, 8000000.00, 2000000.00, 1, 0, '2025-06-30 16:16:04.974983', '2025-06-30 16:16:04.974983', 6),
(4, '9d08a05b247246209d292f21517f0e0f', '2024 Fiscal Year', 'fiscal_year', '2025-01-02', '2025-12-28', 0.00, 0.00, 0.00, 1, 0, '2025-07-01 08:32:00.356427', '2025-07-01 08:32:00.356427', 10),
(5, 'b2c8db6f99104988a67cccbb8d0d7488', 'Demo Period', 'fiscal_year', '2025-07-01', '2025-07-01', 0.00, 0.00, 0.00, 1, 0, '2025-07-01 11:03:13.116226', '2025-07-01 11:03:13.116226', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `budget_budget_report`
--

CREATE TABLE `budget_budget_report` (
  `id` bigint(20) NOT NULL,
  `report_id` char(32) NOT NULL,
  `report_type` varchar(20) NOT NULL,
  `report_title` varchar(200) NOT NULL,
  `report_period_start` date NOT NULL,
  `report_period_end` date NOT NULL,
  `report_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`report_data`)),
  `summary` longtext DEFAULT NULL,
  `report_file` varchar(100) DEFAULT NULL,
  `generated_at` datetime(6) NOT NULL,
  `generated_by_id` bigint(20) NOT NULL,
  `school_budget_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `budget_budget_report`
--

INSERT INTO `budget_budget_report` (`id`, `report_id`, `report_type`, `report_title`, `report_period_start`, `report_period_end`, `report_data`, `summary`, `report_file`, `generated_at`, `generated_by_id`, `school_budget_id`) VALUES
(1, '84a09e303cb4418ab8a2839393413e03', 'monthly', 'Monthly Budget Report 1', '2025-06-01', '2025-07-01', '{\"amount\": 131323}', 'Dummy summary', '', '2025-07-01 08:32:00.556511', 10, 4),
(2, '8dcb14bf3a564142b66f4208fa10c16e', 'monthly', 'Monthly Budget Report 2', '2025-05-02', '2025-06-01', '{\"amount\": 278195}', 'Dummy summary', '', '2025-07-01 08:32:00.559513', 10, 4),
(3, 'db7a07f23ce243a7985e62760b7fb107', 'monthly', 'Monthly Budget Report 3', '2025-04-02', '2025-05-02', '{\"amount\": 335927}', 'Dummy summary', '', '2025-07-01 08:32:00.561513', 10, 4);

-- --------------------------------------------------------

--
-- Table structure for table `budget_budget_transfer`
--

CREATE TABLE `budget_budget_transfer` (
  `id` bigint(20) NOT NULL,
  `transfer_id` char(32) NOT NULL,
  `transfer_type` varchar(20) NOT NULL,
  `transfer_amount` decimal(12,2) NOT NULL,
  `transfer_date` date NOT NULL,
  `reason` longtext NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `approval_date` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_by_id` bigint(20) DEFAULT NULL,
  `created_by_id` bigint(20) NOT NULL,
  `destination_line_item_id` bigint(20) NOT NULL,
  `source_line_item_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `budget_budget_transfer`
--

INSERT INTO `budget_budget_transfer` (`id`, `transfer_id`, `transfer_type`, `transfer_amount`, `transfer_date`, `reason`, `is_approved`, `approval_date`, `created_at`, `updated_at`, `approved_by_id`, `created_by_id`, `destination_line_item_id`, `source_line_item_id`) VALUES
(1, '50053ca9715342b98157fd35b34fa32a', 'within_category', 100000.00, '2025-06-30', 'Reallocate funds for more notebooks', 1, '2025-06-30 16:16:04.992491', '2025-06-30 16:16:04.995310', '2025-06-30 16:16:04.995310', NULL, 6, 2, 1),
(2, 'a7f251038edd4198b66edbbf895d1637', 'within_category', 2000.00, '2025-06-30', 'few set much', 1, '2025-06-30 16:28:35.195400', '2025-06-30 16:16:48.282642', '2025-06-30 16:28:35.198788', 6, 6, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `budget_expenditure`
--

CREATE TABLE `budget_expenditure` (
  `id` bigint(20) NOT NULL,
  `expenditure_id` char(32) NOT NULL,
  `expenditure_type` varchar(20) NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `description` varchar(200) NOT NULL,
  `details` longtext DEFAULT NULL,
  `payment_method` varchar(20) NOT NULL,
  `payment_reference` varchar(100) DEFAULT NULL,
  `payment_date` date NOT NULL,
  `supplier_name` varchar(200) DEFAULT NULL,
  `supplier_contact` varchar(100) DEFAULT NULL,
  `receipt_number` varchar(50) DEFAULT NULL,
  `invoice_number` varchar(50) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_by_id` bigint(20) DEFAULT NULL,
  `budget_line_item_id` bigint(20) NOT NULL,
  `created_by_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `budget_school_budget`
--

CREATE TABLE `budget_school_budget` (
  `id` bigint(20) NOT NULL,
  `budget_id` char(32) NOT NULL,
  `budget_title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `total_budget_amount` decimal(15,2) NOT NULL,
  `allocated_amount` decimal(15,2) NOT NULL,
  `spent_amount` decimal(15,2) NOT NULL,
  `committed_amount` decimal(15,2) NOT NULL,
  `submission_date` datetime(6) DEFAULT NULL,
  `approval_date` datetime(6) DEFAULT NULL,
  `activation_date` datetime(6) DEFAULT NULL,
  `closure_date` datetime(6) DEFAULT NULL,
  `approval_notes` longtext DEFAULT NULL,
  `rejection_reason` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_by_id` bigint(20) DEFAULT NULL,
  `budget_period_id` bigint(20) NOT NULL,
  `created_by_id` bigint(20) NOT NULL,
  `school_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `budget_school_budget`
--

INSERT INTO `budget_school_budget` (`id`, `budget_id`, `budget_title`, `description`, `status`, `total_budget_amount`, `allocated_amount`, `spent_amount`, `committed_amount`, `submission_date`, `approval_date`, `activation_date`, `closure_date`, `approval_notes`, `rejection_reason`, `created_at`, `updated_at`, `approved_by_id`, `budget_period_id`, `created_by_id`, `school_id`) VALUES
(1, '2e10ae7306a0482e8dfc6df16ab48089', 'Help.', 'help students', 'draft', 100000.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, '2025-06-30 15:20:57.666335', '2025-06-30 15:40:50.841937', NULL, 1, 6, 1),
(2, '56ee23154885464898c113f7c291d157', 'Helping', 'for now.', 'approved', 23400.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, '2025-06-30 15:45:56.835831', '2025-06-30 15:56:50.486111', NULL, 1, 6, 1),
(3, '8c65d26f5cf043118b3d5ac783fbf295', 'Test Budget', 'Dummy budget for testing transfers', 'active', 1500000.00, 1500000.00, 500000.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, '2025-06-30 16:16:04.981105', '2025-06-30 16:16:04.981105', NULL, 3, 6, 2),
(4, '35a55d0de2f3430ebd35bfa51fe374ca', '2024 Main Budget', 'Main budget for 2024', 'approved', 10000000.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-01 08:32:00.364774', '2025-07-01 08:32:00.364774', NULL, 4, 10, 3),
(5, '15d794f646d740db9eb2060538af4bce', 'Demo Budget', '', 'approved', 100000.00, 80000.00, 50000.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-01 11:03:21.016552', '2025-07-01 11:03:21.016552', NULL, 5, 13, 5),
(6, '499a672d4fe54166985f57a8916b507b', 'Child care budget', 'This is the budget for this project', 'approved', 120000.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-14 12:57:44.140159', '2025-07-14 12:59:40.858127', NULL, 1, 6, 8);

-- --------------------------------------------------------

--
-- Table structure for table `community_announcement`
--

CREATE TABLE `community_announcement` (
  `id` bigint(20) NOT NULL,
  `announcement_id` char(32) NOT NULL,
  `announcement_type` varchar(20) NOT NULL,
  `priority` varchar(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `summary` longtext DEFAULT NULL,
  `target_audience` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`target_audience`)),
  `publish_date` datetime(6) NOT NULL,
  `expiry_date` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `requires_acknowledgment` tinyint(1) NOT NULL,
  `show_on_dashboard` tinyint(1) NOT NULL,
  `send_email_notification` tinyint(1) NOT NULL,
  `attachments` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`attachments`)),
  `view_count` int(10) UNSIGNED NOT NULL CHECK (`view_count` >= 0),
  `acknowledgment_count` int(10) UNSIGNED NOT NULL CHECK (`acknowledgment_count` >= 0),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `community_announcement`
--

INSERT INTO `community_announcement` (`id`, `announcement_id`, `announcement_type`, `priority`, `title`, `content`, `summary`, `target_audience`, `publish_date`, `expiry_date`, `is_active`, `requires_acknowledgment`, `show_on_dashboard`, `send_email_notification`, `attachments`, `view_count`, `acknowledgment_count`, `created_at`, `updated_at`, `created_by_id`) VALUES
(1, 'bd67812492824d618486e4b9cb1f4236', 'general', 'normal', 'Meeting ahead', 'Hello there', 'Now and then', '[\"admins\", \"auditors\", \"school administration\"]', '2025-06-30 22:00:00.000000', '2025-07-16 22:00:00.000000', 1, 1, 1, 1, '[]', 0, 0, '2025-07-01 07:22:55.604853', '2025-07-01 07:22:55.604853', 6);

-- --------------------------------------------------------

--
-- Table structure for table `community_announcement_target_schools`
--

CREATE TABLE `community_announcement_target_schools` (
  `id` bigint(20) NOT NULL,
  `announcement_id` bigint(20) NOT NULL,
  `school_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `community_community_event`
--

CREATE TABLE `community_community_event` (
  `id` bigint(20) NOT NULL,
  `event_id` char(32) NOT NULL,
  `event_type` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `event_title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `objectives` longtext DEFAULT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `registration_deadline` datetime(6) DEFAULT NULL,
  `location` varchar(200) DEFAULT NULL,
  `is_virtual` tinyint(1) NOT NULL,
  `virtual_meeting_link` varchar(200) DEFAULT NULL,
  `max_participants` int(10) UNSIGNED NOT NULL CHECK (`max_participants` >= 0),
  `current_participants` int(10) UNSIGNED NOT NULL CHECK (`current_participants` >= 0),
  `target_audience` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`target_audience`)),
  `event_materials` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`event_materials`)),
  `view_count` int(10) UNSIGNED NOT NULL CHECK (`view_count` >= 0),
  `registration_count` int(10) UNSIGNED NOT NULL CHECK (`registration_count` >= 0),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `contact_person_id` bigint(20) DEFAULT NULL,
  `created_by_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `community_community_event`
--

INSERT INTO `community_community_event` (`id`, `event_id`, `event_type`, `status`, `event_title`, `description`, `objectives`, `start_date`, `end_date`, `registration_deadline`, `location`, `is_virtual`, `virtual_meeting_link`, `max_participants`, `current_participants`, `target_audience`, `event_materials`, `view_count`, `registration_count`, `created_at`, `updated_at`, `contact_person_id`, `created_by_id`) VALUES
(1, '43cb189be3e14d3db5bee4e4f6f77309', 'meeting', 'in_progress', 'Me and you.', 'To connect students and funders', 'To increase budget', '2025-06-30 22:00:00.000000', '2025-07-08 22:00:00.000000', '2025-07-02 22:00:00.000000', 'Burera', 1, 'https://meet.google.com/vqe-hevn-yrz?ijlm=1751353123841&hs=187&adhoc=1', 200, 0, '[\"user\", \"teachers\"]', '[\"user\", \"teachers\"]', 0, 0, '2025-07-01 06:59:39.182074', '2025-07-01 07:02:08.820191', 7, 6),
(2, '39935d6365a84a09bab1c4e6113a3c63', 'meeting', 'published', 'Awarding preparation', 'This is the meeting for preparing the awarding celemony', 'Have all plans', '2025-07-13 22:00:00.000000', '2025-07-14 22:00:00.000000', '2025-07-13 22:00:00.000000', 'Musanze', 1, 'https://meet.google.com/fea-bxtj-kuu', 9, 0, '[\"admins\", \"auditors\", \"school administration\", \"teachers\"]', '[]', 0, 0, '2025-07-14 13:18:51.074683', '2025-07-14 13:18:51.074683', 4, 6);

-- --------------------------------------------------------

--
-- Table structure for table `community_community_event_organizers`
--

CREATE TABLE `community_community_event_organizers` (
  `id` bigint(20) NOT NULL,
  `communityevent_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `community_community_event_organizers`
--

INSERT INTO `community_community_event_organizers` (`id`, `communityevent_id`, `user_id`) VALUES
(1, 1, 9),
(2, 2, 11),
(3, 2, 12),
(4, 2, 13);

-- --------------------------------------------------------

--
-- Table structure for table `community_community_event_target_schools`
--

CREATE TABLE `community_community_event_target_schools` (
  `id` bigint(20) NOT NULL,
  `communityevent_id` bigint(20) NOT NULL,
  `school_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `community_community_event_target_schools`
--

INSERT INTO `community_community_event_target_schools` (`id`, `communityevent_id`, `school_id`) VALUES
(1, 2, 1),
(2, 2, 3),
(3, 2, 4),
(4, 2, 5),
(5, 2, 6),
(6, 2, 7),
(7, 2, 8);

-- --------------------------------------------------------

--
-- Table structure for table `community_community_forum`
--

CREATE TABLE `community_community_forum` (
  `id` bigint(20) NOT NULL,
  `forum_id` char(32) NOT NULL,
  `forum_name` varchar(200) NOT NULL,
  `forum_type` varchar(20) NOT NULL,
  `access_level` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `rules` longtext DEFAULT NULL,
  `total_topics` int(10) UNSIGNED NOT NULL CHECK (`total_topics` >= 0),
  `total_posts` int(10) UNSIGNED NOT NULL CHECK (`total_posts` >= 0),
  `total_members` int(10) UNSIGNED NOT NULL CHECK (`total_members` >= 0),
  `is_active` tinyint(1) NOT NULL,
  `requires_moderation` tinyint(1) NOT NULL,
  `allow_anonymous` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL,
  `school_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `community_community_forum`
--

INSERT INTO `community_community_forum` (`id`, `forum_id`, `forum_name`, `forum_type`, `access_level`, `description`, `rules`, `total_topics`, `total_posts`, `total_members`, `is_active`, `requires_moderation`, `allow_anonymous`, `created_at`, `updated_at`, `created_by_id`, `school_id`) VALUES
(1, '055317da82364310aff8507d45f36553', 'Cookimg forum', 'general', 'public', 'For analysing food....', 'Not to late..', 0, 0, 0, 1, 1, 1, '2025-07-01 06:43:51.234795', '2025-07-01 06:56:53.808316', 6, 1),
(2, '56239431c9d840f9a74589e8459714d9', 'Organizational', 'grants', 'school_members', 'grants', 'to attend', 0, 0, 0, 1, 1, 1, '2025-07-01 06:57:38.144164', '2025-07-01 06:57:38.144164', 6, 2);

-- --------------------------------------------------------

--
-- Table structure for table `community_community_forum_moderators`
--

CREATE TABLE `community_community_forum_moderators` (
  `id` bigint(20) NOT NULL,
  `communityforum_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `community_community_forum_moderators`
--

INSERT INTO `community_community_forum_moderators` (`id`, `communityforum_id`, `user_id`) VALUES
(1, 1, 3),
(2, 2, 9);

-- --------------------------------------------------------

--
-- Table structure for table `community_community_message`
--

CREATE TABLE `community_community_message` (
  `id` bigint(20) NOT NULL,
  `message_id` char(32) NOT NULL,
  `message_type` varchar(20) NOT NULL,
  `subject` varchar(200) DEFAULT NULL,
  `content` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `is_urgent` tinyint(1) NOT NULL,
  `requires_confirmation` tinyint(1) NOT NULL,
  `attachments` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`attachments`)),
  `read_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `replied_to_id` bigint(20) DEFAULT NULL,
  `school_id` bigint(20) DEFAULT NULL,
  `sender_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `community_community_message`
--

INSERT INTO `community_community_message` (`id`, `message_id`, `message_type`, `subject`, `content`, `status`, `is_urgent`, `requires_confirmation`, `attachments`, `read_at`, `created_at`, `updated_at`, `replied_to_id`, `school_id`, `sender_id`) VALUES
(1, 'd0c18d76e995447e8d5b800b88fb5743', 'direct', 'Withdraw', 'see you in the meet', 'sent', 0, 0, '[]', NULL, '2025-07-01 07:18:02.847041', '2025-07-01 07:18:02.854416', NULL, NULL, 6),
(2, '914de1452f9743ffb0e6138bd8f91137', 'direct', 'Withdraw', 'yes we will be there', 'sent', 0, 0, '[]', NULL, '2025-07-01 07:20:48.943290', '2025-07-01 07:20:48.951896', 1, NULL, 6),
(3, '3008a133361a454896e59cf34a183507', 'direct', 'Deadline is approaching', 'This is the message to remind you that the deadline is ahead', 'sent', 0, 0, '[]', NULL, '2025-07-14 13:23:11.950328', '2025-07-14 13:23:11.962856', NULL, NULL, 6),
(4, '9b0a2c25789942cab644bb4c5c4965b6', 'direct', 'Feedback', 'Thank you', 'sent', 0, 0, '[]', NULL, '2025-07-14 13:24:15.352026', '2025-07-14 13:24:15.363211', 3, NULL, 8);

-- --------------------------------------------------------

--
-- Table structure for table `community_community_message_recipients`
--

CREATE TABLE `community_community_message_recipients` (
  `id` bigint(20) NOT NULL,
  `communitymessage_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `community_community_message_recipients`
--

INSERT INTO `community_community_message_recipients` (`id`, `communitymessage_id`, `user_id`) VALUES
(1, 1, 3),
(3, 3, 8),
(4, 4, 6);

-- --------------------------------------------------------

--
-- Table structure for table `community_feedback`
--

CREATE TABLE `community_feedback` (
  `id` bigint(20) NOT NULL,
  `feedback_id` char(32) NOT NULL,
  `feedback_type` varchar(20) NOT NULL,
  `priority` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `suggestions` longtext DEFAULT NULL,
  `related_module` varchar(50) DEFAULT NULL,
  `submission_date` datetime(6) NOT NULL,
  `review_date` datetime(6) DEFAULT NULL,
  `resolution_date` datetime(6) DEFAULT NULL,
  `response` longtext DEFAULT NULL,
  `resolution_notes` longtext DEFAULT NULL,
  `attachments` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`attachments`)),
  `upvotes` int(10) UNSIGNED NOT NULL CHECK (`upvotes` >= 0),
  `downvotes` int(10) UNSIGNED NOT NULL CHECK (`downvotes` >= 0),
  `view_count` int(10) UNSIGNED NOT NULL CHECK (`view_count` >= 0),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `resolved_by_id` bigint(20) DEFAULT NULL,
  `reviewed_by_id` bigint(20) DEFAULT NULL,
  `school_id` bigint(20) DEFAULT NULL,
  `submitted_by_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `community_forum_post`
--

CREATE TABLE `community_forum_post` (
  `id` bigint(20) NOT NULL,
  `post_id` char(32) NOT NULL,
  `content` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `view_count` int(10) UNSIGNED NOT NULL CHECK (`view_count` >= 0),
  `like_count` int(10) UNSIGNED NOT NULL CHECK (`like_count` >= 0),
  `dislike_count` int(10) UNSIGNED NOT NULL CHECK (`dislike_count` >= 0),
  `attachments` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`attachments`)),
  `is_edited` tinyint(1) NOT NULL,
  `edit_reason` longtext DEFAULT NULL,
  `moderation_notes` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) NOT NULL,
  `edited_by_id` bigint(20) DEFAULT NULL,
  `parent_post_id` bigint(20) DEFAULT NULL,
  `topic_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `community_forum_topic`
--

CREATE TABLE `community_forum_topic` (
  `id` bigint(20) NOT NULL,
  `topic_id` char(32) NOT NULL,
  `topic_title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `view_count` int(10) UNSIGNED NOT NULL CHECK (`view_count` >= 0),
  `reply_count` int(10) UNSIGNED NOT NULL CHECK (`reply_count` >= 0),
  `last_activity` datetime(6) NOT NULL,
  `is_sticky` tinyint(1) NOT NULL,
  `is_announcement` tinyint(1) NOT NULL,
  `allow_replies` tinyint(1) NOT NULL,
  `tags` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`tags`)),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) NOT NULL,
  `forum_id` bigint(20) NOT NULL,
  `last_post_by_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_auditlog`
--

CREATE TABLE `core_auditlog` (
  `id` bigint(20) NOT NULL,
  `action` varchar(10) NOT NULL,
  `object_type` varchar(50) NOT NULL,
  `object_id` varchar(50) NOT NULL,
  `object_repr` varchar(255) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_auditlog`
--

INSERT INTO `core_auditlog` (`id`, `action`, `object_type`, `object_id`, `object_repr`, `timestamp`, `user_id`) VALUES
(1, 'create', 'GrantCategory', '2', 'Electronics (Technology and ICT)', '2025-06-30 13:24:34.343042', 6),
(2, 'update', 'GrantCategory', '4', 'Academic (Technology and ICT)', '2025-06-30 13:36:14.410627', 6),
(3, 'update', 'GrantCategory', '4', 'Academic (Academic Programs)', '2025-06-30 13:36:29.605138', 6),
(4, 'delete', 'GrantCategory', '3', 'Infrastructure (Infrastructure Development)', '2025-06-30 13:36:36.174934', 6);

-- --------------------------------------------------------

--
-- Table structure for table `core_district`
--

CREATE TABLE `core_district` (
  `id` bigint(20) NOT NULL,
  `district_id` char(32) NOT NULL,
  `district_name` varchar(100) NOT NULL,
  `district_code` varchar(10) NOT NULL,
  `province` varchar(100) NOT NULL,
  `total_schools` int(10) UNSIGNED NOT NULL CHECK (`total_schools` >= 0),
  `total_students` int(10) UNSIGNED NOT NULL CHECK (`total_students` >= 0),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_school`
--

CREATE TABLE `core_school` (
  `id` bigint(20) NOT NULL,
  `school_id` char(32) NOT NULL,
  `school_name` varchar(200) NOT NULL,
  `school_code` varchar(20) NOT NULL,
  `district` varchar(100) NOT NULL,
  `sector` varchar(100) NOT NULL,
  `cell` varchar(100) NOT NULL,
  `village` varchar(100) NOT NULL,
  `level` varchar(20) NOT NULL,
  `total_students` int(10) UNSIGNED NOT NULL CHECK (`total_students` >= 0),
  `total_teachers` int(10) UNSIGNED NOT NULL CHECK (`total_teachers` >= 0),
  `total_staff` int(10) UNSIGNED NOT NULL CHECK (`total_staff` >= 0),
  `phone_number` varchar(15) DEFAULT NULL,
  `email_address` varchar(254) DEFAULT NULL,
  `website` varchar(200) DEFAULT NULL,
  `address` longtext NOT NULL,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `principal_name` varchar(100) DEFAULT NULL,
  `principal_phone` varchar(15) DEFAULT NULL,
  `principal_email` varchar(254) DEFAULT NULL,
  `academic_performance_score` decimal(5,2) NOT NULL,
  `infrastructure_score` decimal(5,2) NOT NULL,
  `need_score` decimal(5,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_school`
--

INSERT INTO `core_school` (`id`, `school_id`, `school_name`, `school_code`, `district`, `sector`, `cell`, `village`, `level`, `total_students`, `total_teachers`, `total_staff`, `phone_number`, `email_address`, `website`, `address`, `latitude`, `longitude`, `status`, `principal_name`, `principal_phone`, `principal_email`, `academic_performance_score`, `infrastructure_score`, `need_score`, `created_at`, `updated_at`, `created_by_id`) VALUES
(1, '494d65ae892b43dabc407c4303e87c7a', 'RP tumba college', '2024-Tumba', 'Rulindo', 'Bushoke', 'Tumba', 'Bushoke', 'upper_secondary', 2000, 50, 80, '0791724884', 'tumba@gmail.com', 'http://tumba.com', 'NR501\r\nNR502', NULL, NULL, 'active', NULL, NULL, NULL, 90.00, 69.98, 49.95, '2025-06-30 13:50:39.780156', '2025-06-30 13:50:39.780156', 6),
(2, '6ab30d45e05749c1b6346c6f3eb9fb43', 'Test School', '', '', '', '', '', 'both', 0, 0, 0, NULL, NULL, NULL, '', NULL, NULL, 'active', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-06-30 16:16:04.971166', '2025-06-30 16:16:04.971166', NULL),
(3, '1518f05cbc0848d89f4af22d37890ef2', 'Dummy Secondary School', 'SCH001', 'Kigali', 'Gasabo', 'Kacyiru', 'Village A', 'both', 0, 0, 0, NULL, NULL, NULL, '123 Main St', NULL, NULL, 'active', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 08:32:00.348210', '2025-07-01 08:32:00.348210', 10),
(4, 'c1bacf2a157046c89574014903038c72', 'Dummy School Kigali', 'SCH002', 'Kigali', 'Sector X', 'Cell Y', 'Village Z', 'both', 0, 0, 0, NULL, NULL, NULL, 'Kigali Main St', NULL, NULL, 'active', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.394249', '2025-07-01 09:04:53.394249', 10),
(5, 'bc143904f2de434cb7b3063ebe2451cf', 'Dummy School Eastern', 'SCH003', 'Eastern', 'Sector X', 'Cell Y', 'Village Z', 'both', 0, 0, 0, NULL, NULL, NULL, 'Eastern Main St', NULL, NULL, 'active', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.413389', '2025-07-01 09:04:53.413389', 10),
(6, 'e972f0cf09034eb9829a18cf156cfc73', 'Dummy School Western', 'SCH004', 'Western', 'Sector X', 'Cell Y', 'Village Z', 'both', 0, 0, 0, NULL, NULL, NULL, 'Western Main St', NULL, NULL, 'active', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.424613', '2025-07-01 09:04:53.424613', 10),
(7, 'b81158a4fd2e4159b019b92fc67181b6', 'Dummy School Southern', 'SCH005', 'Southern', 'Sector X', 'Cell Y', 'Village Z', 'both', 0, 0, 0, NULL, NULL, NULL, 'Southern Main St', NULL, NULL, 'active', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.437242', '2025-07-01 09:04:53.437242', 10),
(8, '05c3810b98c34b35acd9363bc2188cb2', 'Dummy School Northern', 'SCH006', 'Northern', 'Sector X', 'Cell Y', 'Village Z', 'both', 0, 0, 0, NULL, NULL, NULL, 'Northern Main St', NULL, NULL, 'active', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.453356', '2025-07-01 09:04:53.453356', 10);

-- --------------------------------------------------------

--
-- Table structure for table `core_school_user`
--

CREATE TABLE `core_school_user` (
  `id` bigint(20) NOT NULL,
  `school_role` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `can_submit_proposals` tinyint(1) NOT NULL,
  `can_manage_budget` tinyint(1) NOT NULL,
  `can_view_reports` tinyint(1) NOT NULL,
  `can_manage_users` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `assigned_by_id` bigint(20) DEFAULT NULL,
  `school_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_system_configuration`
--

CREATE TABLE `core_system_configuration` (
  `id` bigint(20) NOT NULL,
  `config_key` varchar(100) NOT NULL,
  `config_value` longtext NOT NULL,
  `config_type` varchar(20) NOT NULL,
  `category` varchar(20) NOT NULL,
  `description` longtext DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_system` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_user`
--

CREATE TABLE `core_user` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `user_id` char(32) NOT NULL,
  `role` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `address` longtext DEFAULT NULL,
  `emergency_contact` varchar(15) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `last_login_ip` char(39) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_user`
--

INSERT INTO `core_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `user_id`, `role`, `status`, `phone_number`, `profile_picture`, `date_of_birth`, `address`, `emergency_contact`, `created_at`, `updated_at`, `last_login_ip`) VALUES
(2, 'pbkdf2_sha256$600000$78lAjl7XtzSehcoddPFUVi$/GCj3k/oJ9Oh4Wj33l2qx282SY9vCSl/vLI4zy+3+gw=', '2025-06-29 19:52:06.667623', 0, 'jado-dusengimana', 'Hozana', 'DUSABIMANA', 'jado@gmail.com', 1, 1, '2025-06-29 18:45:12.020766', '2ed360f716564b04bfd39e8f818f57e9', 'school_admin', 'active', NULL, '', NULL, NULL, NULL, '2025-06-29 18:45:12.337625', '2025-07-01 11:40:18.727213', NULL),
(3, 'pbkdf2_sha256$600000$7UTDk2SRmvkeblaM9WYDgx$iWOpgTsao9XgAJauhlRz5z8yB/8OEs0MXB2LJMPfmps=', '2025-06-30 11:52:53.860767', 0, 'Hozan', 'Hozana', 'DUSABIMANA', 'dhozana559@gmail.com', 0, 1, '2025-06-30 11:09:22.519523', '61ed5ca885004906ab7646f9df245774', 'auditor', 'pending', NULL, '', NULL, NULL, NULL, '2025-06-30 11:09:22.833517', '2025-06-30 11:09:22.833517', NULL),
(4, 'pbkdf2_sha256$600000$jLNSx59sKFVxpnSs2vVTpM$yylFQPMp8s88BWC0WX4ntuoBtXQrp9qStF6EsC2zGko=', '2025-06-30 12:49:38.305543', 0, 'Administrator2', 'Hozana', 'DUSABIMANA', 'admini@gmail.com', 1, 1, '2025-06-30 12:32:55.811852', '1895bf1578bc438fa85d0c322580b1d3', 'school_admin', 'active', NULL, '', NULL, NULL, NULL, '2025-06-30 12:32:56.112851', '2025-07-01 11:40:18.727213', NULL),
(5, 'pbkdf2_sha256$600000$fSMwB3SyJmUvjHDDSSAlIe$mDwx5hUBDiRm4+RS/68qeNSERwMxg8V+TzIq7AOrBOo=', '2025-07-14 05:18:14.763235', 0, 'Grant-admin', 'Hozana', 'DUSABIMANA', 'admin@gmail.com', 1, 1, '2025-06-30 12:54:50.664282', '73fc559eaba84199b9dfc9e60f72dec2', 'reb_official', 'pending', NULL, '', NULL, NULL, NULL, '2025-06-30 12:54:50.975379', '2025-06-30 12:54:50.975379', NULL),
(6, 'pbkdf2_sha256$600000$KOu0VUoyP0TT8iGKcw9XNO$8sQLJG/+D11VcS9LE/+gm647jcqZ1GW2Ptpj7eiyrs8=', '2025-07-16 08:59:22.399115', 1, 'admin', '', '', 'admin06@gmail.com', 1, 1, '2025-06-30 13:14:59.682590', '455f0aca614d43b0aae99dc59a832f2f', 'system_admin', 'active', NULL, '', NULL, NULL, NULL, '2025-06-30 13:14:59.976710', '2025-07-01 11:40:11.583622', NULL),
(7, 'pbkdf2_sha256$600000$KOu0VUoyP0TT8iGKcw9XNO$8sQLJG/+D11VcS9LE/+gm647jcqZ1GW2Ptpj7eiyrs8=', '2025-07-01 11:35:34.258752', 1, 'reb-officer', '', '', 'reb-officer@reb.gov.rw', 1, 1, '2025-06-30 13:21:02.979737', '2d8b18601a14450192f63d8202e6ec2c', 'reb_officer', 'active', NULL, '', NULL, NULL, NULL, '2025-06-30 13:21:02.979737', '2025-07-01 11:40:11.583622', NULL),
(8, 'pbkdf2_sha256$600000$KOu0VUoyP0TT8iGKcw9XNO$8sQLJG/+D11VcS9LE/+gm647jcqZ1GW2Ptpj7eiyrs8=', '2025-07-14 13:56:02.457905', 0, 'school-admin', '', '', 'school-admin@school.rw', 1, 1, '2025-06-30 13:21:09.551307', 'da700e35a8774ad086ef476c24f7de4c', 'school_admin', 'active', NULL, '', NULL, NULL, NULL, '2025-06-30 13:21:09.551307', '2025-07-01 11:40:18.727213', NULL),
(9, 'pbkdf2_sha256$600000$KOu0VUoyP0TT8iGKcw9XNO$8sQLJG/+D11VcS9LE/+gm647jcqZ1GW2Ptpj7eiyrs8=', '2025-07-15 18:50:17.062110', 0, 'teacher', '', '', 'teacher@school.rw', 0, 1, '2025-06-30 13:21:11.277053', 'e67d9aca97cc481ca7d3bb3a6221a074', 'teacher', 'active', NULL, '', NULL, NULL, NULL, '2025-06-30 13:21:11.277053', '2025-07-01 11:40:27.147505', NULL),
(10, 'pbkdf2_sha256$600000$KOu0VUoyP0TT8iGKcw9XNO$8sQLJG/+D11VcS9LE/+gm647jcqZ1GW2Ptpj7eiyrs8=', NULL, 1, 'dummy_reb_officer', 'Reb_officer', 'User', 'reb_officer@example.com', 1, 1, '2025-07-01 08:32:00.334094', 'a9977da300e247e7961dc7b7af2654a3', 'reb_officer', 'active', NULL, '', NULL, NULL, NULL, '2025-07-01 08:32:00.334094', '2025-07-01 11:40:11.583622', NULL),
(11, 'pbkdf2_sha256$600000$KOu0VUoyP0TT8iGKcw9XNO$8sQLJG/+D11VcS9LE/+gm647jcqZ1GW2Ptpj7eiyrs8=', NULL, 0, 'dummy_school_admin', 'School_admin', 'User', 'school_admin@example.com', 1, 1, '2025-07-01 08:32:00.340707', '468c64557d5c4c79b4d4b1e057d7a9b2', 'school_admin', 'active', NULL, '', NULL, NULL, NULL, '2025-07-01 08:32:00.340707', '2025-07-01 11:40:18.719209', NULL),
(12, 'pbkdf2_sha256$600000$KOu0VUoyP0TT8iGKcw9XNO$8sQLJG/+D11VcS9LE/+gm647jcqZ1GW2Ptpj7eiyrs8=', NULL, 0, 'dummy_teacher', 'Teacher', 'User', 'teacher@example.com', 0, 1, '2025-07-01 08:32:00.343242', '10887e8ee40542cf912d9b46aaaac3e3', 'teacher', 'active', NULL, '', NULL, NULL, NULL, '2025-07-01 08:32:00.343242', '2025-07-14 05:23:18.285233', NULL),
(13, 'pbkdf2_sha256$600000$KOu0VUoyP0TT8iGKcw9XNO$8sQLJG/+D11VcS9LE/+gm647jcqZ1GW2Ptpj7eiyrs8=', NULL, 1, 'dummy_system_admin', 'System_admin', 'User', 'system_admin@example.com', 1, 1, '2025-07-01 08:32:00.345209', '2d95771acf53491a88e82de4ea32323e', 'system_admin', 'active', NULL, '', NULL, NULL, NULL, '2025-07-01 08:32:00.345209', '2025-07-01 11:40:11.575583', NULL),
(16, 'pbkdf2_sha256$600000$aE1L5S4FgnzNO8mkpX7ftg$t0XaKIoVHbIq29sNDktX0UY0WTKodXpTv9CMz5OJtp4=', NULL, 0, '22rp01605', 'Hozana', 'DUSABIMANA', 'dhozana559@gmail.com', 0, 1, '2025-07-14 05:29:12.093654', '4683e92caf174352bf581e3d06ce0dc6', 'school_admin', 'active', '0791724884', '', NULL, 'NR501\r\nNR502', '12345', '2025-07-14 05:29:12.553844', '2025-07-14 05:31:15.543899', NULL),
(17, 'pbkdf2_sha256$600000$hfATxkzy5kb7YEnflA4UVo$ZYKEdqMrvhgnXW8dTCediZo+ccv3cMbgshYYqsEkJ6A=', '2025-07-15 18:22:46.492423', 0, 'hozana', 'DUSABIMANA', 'Hozana', 'suppliyer@gmail.com', 0, 1, '2025-07-15 18:22:35.218558', '19e8a117f3e34627aa2dea0b75e7739c', 'supplier', 'pending', NULL, '', NULL, NULL, NULL, '2025-07-15 18:22:35.522013', '2025-07-15 18:22:35.522013', NULL),
(18, 'pbkdf2_sha256$600000$qJSkbyfNkLc8WwLAihVBpI$NlYovGm0BWUSXmNuFyYkWmezZCG1pw1TG9ekVYEKEio=', '2025-07-16 08:54:22.753601', 0, 'hozana1', 'DUSABIMANA', 'Hozana', 'suppliyer12@gmail.com', 0, 1, '2025-07-16 08:54:18.983655', 'e3e915072402421ea4382877c4ea056e', 'supplier', 'pending', NULL, '', NULL, NULL, NULL, '2025-07-16 08:54:19.421171', '2025-07-16 08:54:19.421171', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `core_user_groups`
--

CREATE TABLE `core_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_user_user_permissions`
--

CREATE TABLE `core_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_user_user_permissions`
--

INSERT INTO `core_user_user_permissions` (`id`, `user_id`, `permission_id`) VALUES
(62, 2, 21),
(63, 2, 22),
(64, 2, 23),
(65, 2, 24),
(58, 2, 45),
(59, 2, 46),
(60, 2, 47),
(61, 2, 48),
(66, 2, 89),
(67, 2, 90),
(68, 2, 91),
(69, 2, 92),
(50, 4, 21),
(51, 4, 22),
(52, 4, 23),
(53, 4, 24),
(46, 4, 45),
(47, 4, 46),
(48, 4, 47),
(49, 4, 48),
(54, 4, 89),
(55, 4, 90),
(56, 4, 91),
(57, 4, 92),
(38, 8, 21),
(39, 8, 22),
(40, 8, 23),
(41, 8, 24),
(34, 8, 45),
(35, 8, 46),
(36, 8, 47),
(37, 8, 48),
(42, 8, 89),
(43, 8, 90),
(44, 8, 91),
(45, 8, 92),
(10, 9, 44),
(12, 9, 48),
(8, 9, 72),
(14, 9, 92),
(9, 9, 136),
(11, 9, 141),
(13, 9, 144),
(26, 11, 21),
(27, 11, 22),
(28, 11, 23),
(29, 11, 24),
(22, 11, 45),
(23, 11, 46),
(24, 11, 47),
(25, 11, 48),
(30, 11, 89),
(31, 11, 90),
(32, 11, 91),
(33, 11, 92),
(3, 12, 44),
(5, 12, 48),
(1, 12, 72),
(7, 12, 92),
(2, 12, 136),
(4, 12, 141),
(6, 12, 144);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-06-30 13:17:59.460618', '1', 'Software deveopment (Technology and ICT)', 1, '[{\"added\": {}}]', 11, 6),
(2, '2025-06-30 13:50:39.781191', '1', 'RP tumba college (2024-Tumba)', 1, '[{\"added\": {}}]', 8, 6),
(3, '2025-07-02 11:44:46.568186', '7', 'Mobile applications (Sports and Recreation)', 1, '[{\"added\": {}}]', 11, 6);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(57, 'ai_engine', 'aimodelstatus'),
(48, 'ai_engine', 'aiperformancemetrics'),
(49, 'ai_engine', 'allocationalgorithm'),
(50, 'ai_engine', 'allocationfactor'),
(51, 'ai_engine', 'allocationrun'),
(52, 'ai_engine', 'optimizationrecommendation'),
(53, 'ai_engine', 'proposalallocationscore'),
(58, 'ai_engine', 'proposalanomaly'),
(59, 'ai_engine', 'proposalprediction'),
(56, 'ai_engine', 'recommendationaction'),
(54, 'ai_engine', 'riskassessment'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(17, 'budget', 'budgetcategory'),
(18, 'budget', 'budgetlineitem'),
(19, 'budget', 'budgetperiod'),
(20, 'budget', 'budgetreport'),
(21, 'budget', 'budgettransfer'),
(22, 'budget', 'expenditure'),
(23, 'budget', 'schoolbudget'),
(41, 'community', 'announcement'),
(42, 'community', 'communityevent'),
(43, 'community', 'communityforum'),
(44, 'community', 'communitymessage'),
(45, 'community', 'feedback'),
(46, 'community', 'forumpost'),
(47, 'community', 'forumtopic'),
(4, 'contenttypes', 'contenttype'),
(55, 'core', 'auditlog'),
(7, 'core', 'district'),
(8, 'core', 'school'),
(10, 'core', 'schooluser'),
(9, 'core', 'systemconfiguration'),
(6, 'core', 'user'),
(16, 'grants', 'fundallocation'),
(11, 'grants', 'grantcategory'),
(12, 'grants', 'grantproposal'),
(15, 'grants', 'proposalbudget'),
(14, 'grants', 'proposaldocument'),
(13, 'grants', 'proposalreview'),
(63, 'procurement', 'bid'),
(61, 'procurement', 'tender'),
(62, 'procurement', 'tenderdocument'),
(60, 'procurement', 'tenderstatushistory'),
(30, 'reporting', 'analyticsevent'),
(24, 'reporting', 'dashboard'),
(29, 'reporting', 'dashboardwidget'),
(28, 'reporting', 'dataexport'),
(25, 'reporting', 'kpi'),
(31, 'reporting', 'kpivalue'),
(65, 'reporting', 'proposalcriterion'),
(68, 'reporting', 'proposalcriterionresponse'),
(64, 'reporting', 'rebgrantbudget'),
(26, 'reporting', 'report'),
(27, 'reporting', 'reportschedule'),
(66, 'reporting', 'suppliercriterion'),
(67, 'reporting', 'suppliercriterionresponse'),
(5, 'sessions', 'session'),
(39, 'training', 'assessmentresult'),
(32, 'training', 'coursemodule'),
(40, 'training', 'moduleprogress'),
(38, 'training', 'trainingassessment'),
(33, 'training', 'trainingcategory'),
(37, 'training', 'trainingcertificate'),
(34, 'training', 'trainingcourse'),
(36, 'training', 'trainingenrollment'),
(35, 'training', 'trainingsession');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-06-29 18:00:36.325106'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-06-29 18:00:36.371640'),
(3, 'auth', '0001_initial', '2025-06-29 18:00:36.545142'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-06-29 18:00:36.579463'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-06-29 18:00:36.583466'),
(6, 'auth', '0004_alter_user_username_opts', '2025-06-29 18:00:36.588780'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-06-29 18:00:36.592789'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-06-29 18:00:36.593943'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-06-29 18:00:36.597596'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-06-29 18:00:36.602598'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-06-29 18:00:36.607694'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-06-29 18:00:36.614818'),
(13, 'auth', '0011_update_proxy_permissions', '2025-06-29 18:00:36.620819'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-06-29 18:00:36.624817'),
(15, 'core', '0001_initial', '2025-06-29 18:00:37.107703'),
(16, 'admin', '0001_initial', '2025-06-29 18:00:37.182083'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-06-29 18:00:37.191205'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-06-29 18:00:37.199204'),
(19, 'grants', '0001_initial', '2025-06-29 18:00:37.879540'),
(20, 'ai_engine', '0001_initial', '2025-06-29 18:00:38.038251'),
(21, 'ai_engine', '0002_initial', '2025-06-29 18:00:38.740247'),
(22, 'budget', '0001_initial', '2025-06-29 18:00:38.880326'),
(23, 'budget', '0002_initial', '2025-06-29 18:00:39.844376'),
(24, 'community', '0001_initial', '2025-06-29 18:00:40.049436'),
(25, 'community', '0002_initial', '2025-06-29 18:00:41.688150'),
(26, 'reporting', '0001_initial', '2025-06-29 18:00:42.724528'),
(27, 'sessions', '0001_initial', '2025-06-29 18:00:42.750970'),
(28, 'training', '0001_initial', '2025-06-29 18:00:44.164219'),
(29, 'core', '0002_auditlog', '2025-06-30 13:08:43.410456'),
(30, 'ai_engine', '0003_recommendationaction', '2025-07-01 09:48:41.126634'),
(31, 'ai_engine', '0004_aimodelstatus', '2025-07-01 10:14:10.673737'),
(32, 'ai_engine', '0005_proposalprediction_proposalanomaly', '2025-07-01 10:22:45.582542'),
(33, 'procurement', '0001_initial', '2025-07-14 04:51:56.601406'),
(34, 'grants', '0002_proposaldocument_ocr_text', '2025-07-15 17:33:30.178258'),
(35, 'core', '0003_alter_user_role', '2025-07-15 18:08:53.590938'),
(36, 'procurement', '0002_bid', '2025-07-15 18:10:08.325199'),
(37, 'training', '0002_trainingcourse_guide_document_and_more', '2025-07-15 18:30:33.084017'),
(38, 'reporting', '0002_rebgrantbudget', '2025-07-16 06:58:24.011128'),
(39, 'reporting', '0003_proposalcriterion_suppliercriterion', '2025-07-16 07:28:49.570767'),
(40, 'reporting', '0004_suppliercriterionresponse_proposalcriterionresponse', '2025-07-16 07:41:24.233267');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('1dxtedyugajyltsvlqx04dsvncuxi1ze', '.eJxVjMsOwiAUBf-FtSFQKQWX7v0GcrkPqRqalHZl_HfbpAvdnpk5b5VgXUpaG89pJHVRNqjT75gBn1x3Qg-o90njVJd5zHpX9EGbvk3Er-vh_h0UaGWrXQxD7IKQY3Hc9z5YAbKYWYwY2pA1QnYAdtTlGM8AEb2BHD0KsqjPFx0xOT8:1ubxuA:6ZO26hRhLX-2-x_-H3gPD2jg2T-0qY19b766rHeZLWk', '2025-07-16 09:54:22.755629'),
('2u7rcaiadt2rphsml68xh2spbbk3ckzy', '.eJxVjMsOgkAMRf9l1mYCFobWpXu-gbSdVlADCY-V8d-VhIVu7znnvkLH29p322JzN-RwCSmcfjdhfdi4g3zn8TZFncZ1HiTuSjzoEtsp2_N6uH8HPS_9t8ZcIWEqQLByMCZEOJei6rW5N8khuXhDyMZaAChCmYkoodRKJuH9Aez9OGw:1uWGNq:kFsn46JuTWEGfeAwaX0SQHw1CvcasZ75P-n7ltG4h6g', '2025-06-30 16:25:26.270479'),
('4riuhpr4ps8epucfztoqc7ozd8ucr49i', '.eJxVjMEOwiAQRP-FsyFAKbgevfsNzS67SNXQpLQn47_bJj3oYS7z3sxbDbguZVibzMPI6qKCOv12hOkpdQf8wHqfdJrqMo-kd0UftOnbxPK6Hu7fQcFWtrU4ps70FD32gdECgZNs8xZ2EbJ1ls5AHXjocwSPhimKC9kkQ-Q79fkC9nI4Ng:1ubBa8:e-WsnC4N-qsjox5gFwRjJK5uW8v-RYnx7ziGY_SCjuo', '2025-07-14 06:18:28.473626'),
('7aq91orxhz34p9gk33syg2sxg7o6fk37', '.eJxVjMEOwiAQRP-FsyFAKbgevfsNzS67SNXQpLQn47_bJj3oYS7z3sxbDbguZVibzMPI6qKCOv12hOkpdQf8wHqfdJrqMo-kd0UftOnbxPK6Hu7fQcFWtrU4ps70FD32gdECgZNs8xZ2EbJ1ls5AHXjocwSPhimKC9kkQ-Q79fkC9nI4Ng:1ubJhN:PyP_cGnC_P8LxmqYrFO0b3uYSGDmnNjuJKtnGR9lga4', '2025-07-14 14:58:29.869879'),
('8r5q6eml65otry7lyjst4nvp3qlsjfyr', '.eJxVjMEOwiAQRP-FsyFAKbgevfsNzS67SNXQpLQn47_bJj3oYS7z3sxbDbguZVibzMPI6qKCOv12hOkpdQf8wHqfdJrqMo-kd0UftOnbxPK6Hu7fQcFWtrU4ps70FD32gdECgZNs8xZ2EbJ1ls5AHXjocwSPhimKC9kkQ-Q79fkC9nI4Ng:1ubLwc:8Mo-Z2E9tOqXD43nkX5fwvJVin7Js4BrnAWa3vDXHq4', '2025-07-14 17:22:22.462265'),
('91z4cagrrvhog14ncb4s0dmbpf1dbibe', '.eJxVjMsOgkAMRf9l1mYCFobWpXu-gbSdVlADCY-V8d-VhIVu7znnvkLH29p322JzN-RwCSmcfjdhfdi4g3zn8TZFncZ1HiTuSjzoEtsp2_N6uH8HPS_9t8ZcIWEqQLByMCZEOJei6rW5N8khuXhDyMZaAChCmYkoodRKJuH9Aez9OGw:1uWJZX:499Ty_xrpqmwWyMYG5zYCSpO9WxnkLA05osA3SAdoHU', '2025-06-30 19:49:43.106434'),
('ai8zrhsu8hn27pdyadrmpgoh43b0osyg', '.eJxVjMEOwiAQRP-FsyFAKbgevfsNzS67SNXQpLQn47_bJj3oYS7z3sxbDbguZVibzMPI6qKCOv12hOkpdQf8wHqfdJrqMo-kd0UftOnbxPK6Hu7fQcFWtrU4ps70FD32gdECgZNs8xZ2EbJ1ls5AHXjocwSPhimKC9kkQ-Q79fkC9nI4Ng:1uWfqN:t0jgW1nhvll4aeg39JewguvcJ1FoMfeyZCrNNleIbJY', '2025-07-01 19:36:35.173145'),
('ajqqbajz60wohexaqjvzj41pxcayui77', '.eJxVjMEOwiAQRP-FsyFAKbgevfsNzS67SNXQpLQn47_bJj3oYS7z3sxbDbguZVibzMPI6qKCOv12hOkpdQf8wHqfdJrqMo-kd0UftOnbxPK6Hu7fQcFWtrU4ps70FD32gdECgZNs8xZ2EbJ1ls5AHXjocwSPhimKC9kkQ-Q79fkC9nI4Ng:1ubkR7:jZr8_c3_DZw7sQvnojAKnFu1Xr5Tze64kun74eeo8e0', '2025-07-15 19:31:29.879999'),
('e3i9k7xi7wd2v82kcyvrgkrwxaydtxsi', '.eJxVjMEOwiAQRP-FsyFAKbgevfsNzS67SNXQpLQn47_bJj3oYS7z3sxbDbguZVibzMPI6qKCOv12hOkpdQf8wHqfdJrqMo-kd0UftOnbxPK6Hu7fQcFWtrU4ps70FD32gdECgZNs8xZ2EbJ1ls5AHXjocwSPhimKC9kkQ-Q79fkC9nI4Ng:1ubfcP:VF5ULbMZM-GLmUmPGcF1tPj5o_t5JPm662SUVZmpOeY', '2025-07-15 14:22:49.987770'),
('evcgr43oi6gi9882g9imlrrlc16wv96g', '.eJxVjMEOwiAQRP-FsyFAKbgevfsNzS67SNXQpLQn47_bJj3oYS7z3sxbDbguZVibzMPI6qKCOv12hOkpdQf8wHqfdJrqMo-kd0UftOnbxPK6Hu7fQcFWtrU4ps70FD32gdECgZNs8xZ2EbJ1ls5AHXjocwSPhimKC9kkQ-Q79fkC9nI4Ng:1ubjQN:m0zUxMb4Cdec8rVzNliQ9vsAD9Q718q057WrktoWko8', '2025-07-15 18:26:39.968398'),
('flx8e3zndxq2afnwcv5hrwo37mnaf8uh', '.eJxVjMsOgkAMRf9l1mYCFobWpXu-gbSdVlADCY-V8d-VhIVu7znnvkLH29p322JzN-RwCSmcfjdhfdi4g3zn8TZFncZ1HiTuSjzoEtsp2_N6uH8HPS_9t8ZcIWEqQLByMCZEOJei6rW5N8khuXhDyMZaAChCmYkoodRKJuH9Aez9OGw:1uWFQa:SLWG_TiNGrDNdcXlwQzDI5hMl5LDXI02KnS4RpjKDV8', '2025-06-30 15:24:12.466780'),
('g2hw3jcl32pl4fabz79eex5xc10o16cl', '.eJxVjMEOwiAQRP-FsyFAKbgevfsNzS67SNXQpLQn47_bJj3oYS7z3sxbDbguZVibzMPI6qKCOv12hOkpdQf8wHqfdJrqMo-kd0UftOnbxPK6Hu7fQcFWtrU4ps70FD32gdECgZNs8xZ2EbJ1ls5AHXjocwSPhimKC9kkQ-Q79fkC9nI4Ng:1ubwzR:Y9fCbOrWo4y1F5ADc4DOny4zKipPvBEsPIT-T7Fh4go', '2025-07-16 08:55:45.264591'),
('gbqsw3ft4simkfo0agkg8r5uzjrwjutq', '.eJxVjMEOwiAQRP-FsyFAKbgevfsNzS67SNXQpLQn47_bJj3oYS7z3sxbDbguZVibzMPI6qKCOv12hOkpdQf8wHqfdJrqMo-kd0UftOnbxPK6Hu7fQcFWtrU4ps70FD32gdECgZNs8xZ2EbJ1ls5AHXjocwSPhimKC9kkQ-Q79fkC9nI4Ng:1ubw2X:woRcDbUYgvornSs9pl3ebMCrPfRExOA-162xuAM1AzM', '2025-07-16 07:54:53.122529'),
('j9im0rzzc8v9dsf4r2daebo6j3v5y3ag', '.eJxVjMsOgkAMRf9l1mYCFobWpXu-gbSdVlADCY-V8d-VhIVu7znnvkLH29p322JzN-RwCSmcfjdhfdi4g3zn8TZFncZ1HiTuSjzoEtsp2_N6uH8HPS_9t8ZcIWEqQLByMCZEOJei6rW5N8khuXhDyMZaAChCmYkoodRKJuH9Aez9OGw:1uWKVm:RNY_DabMsoYaLUTLt1qdHIep0IdMCrP8RMzisw6FS-A', '2025-06-30 20:49:54.629697'),
('joox0at6wjfi30x6qj7s9jpjintimeqq', '.eJyFzbFuAjEMgOFXOWWuTkAgOIxdmEBIDIwnx3F6V1CCkhwMiHcnSAdqVRVW-_Pvi2iwz23TJ45NZ8VCKPHxc2aQ9uzvC_uN_ivUFHyOnanvpB62qV4Fy4fPwf4KtJjacg12ChrUSBqYOsmoAeRkbIjcjJ2bKyeVM26uARlpJCWBHFuttQIzI82mRCNTg5S74JNYXMQyos_VJoZjSHio1iHmlqOvZPkW-dTxudz8hyYFIREf81-0Df370hO9Ku045UdoMNfrDQNkfRc:1uWXay:t9_NnZKsB1fIw-Cx85VYHPvc72v4JT5N00fixYf9mYU', '2025-07-01 10:48:08.896930'),
('p9lxrbmu8hq9844352gx5e6epljfl0vb', '.eJxVjMEOwiAQRP-FsyFAKbgevfsNzS67SNXQpLQn47_bJj3oYS7z3sxbDbguZVibzMPI6qKCOv12hOkpdQf8wHqfdJrqMo-kd0UftOnbxPK6Hu7fQcFWtrU4ps70FD32gdECgZNs8xZ2EbJ1ls5AHXjocwSPhimKC9kkQ-Q79fkC9nI4Ng:1uWvqK:g5v-Hzx5VbI-wyYkeuaTdPvI56Lt95jhBXHuSfKoKYo', '2025-07-02 12:41:36.203300'),
('qq7mvggl8mjxc36cjmc0h1j0axgqvwvw', '.eJxVjMEOwiAQRP-FsyFAKbgevfsNzS67SNXQpLQn47_bJj3oYS7z3sxbDbguZVibzMPI6qKCOv12hOkpdQf8wHqfdJrqMo-kd0UftOnbxPK6Hu7fQcFWtrU4ps70FD32gdECgZNs8xZ2EbJ1ls5AHXjocwSPhimKC9kkQ-Q79fkC9nI4Ng:1ubIhO:W0FQ8FtMIv_Ms86MrV7ZLeD0TfOolRz24b2GQ00-drg', '2025-07-14 13:54:26.368681'),
('rqmlzfmwo2x33nwt9f2vruax7m196swf', '.eJxVjMsOgkAMRf9l1mYCFobWpXu-gbSdVlADCY-V8d-VhIVu7znnvkLH29p322JzN-RwCSmcfjdhfdi4g3zn8TZFncZ1HiTuSjzoEtsp2_N6uH8HPS_9t8ZcIWEqQLByMCZEOJei6rW5N8khuXhDyMZaAChCmYkoodRKJuH9Aez9OGw:1uWETv:1WEnRkGVvwYkVOFGRSylh56D2e_KetDlBXnTyaU3uOc', '2025-06-30 14:23:35.971229'),
('siduddhnkh1aivx6abzv2ors8jv1dmox', '.eJxVjEEOwiAQRe_C2pAyhVJduvcMZGBmpGogKe3KeHdD0oVu_3vvv1XAfcthb7yGhdRFgTr9bhHTk0sH9MByrzrVsq1L1F3RB236Volf18P9O8jYcq-NIIik5ObBmTFaIJ4ZPCBRAp5I6GzsIM56YUGxTvwILvKUyEYf1ecLFS45Uw:1uVx1w:3-U1CHzjiywEppCuQ_bQHTrI057znGL8A1llP2b5bMQ', '2025-06-29 19:45:32.391797'),
('tlfb7i8g7ku6qyzfppn0kkp464letnvx', '.eJxVjMsOgkAMRf9l1mYCFobWpXu-gbSdVlADCY-V8d-VhIVu7znnvkLH29p322JzN-RwCSmcfjdhfdi4g3zn8TZFncZ1HiTuSjzoEtsp2_N6uH8HPS_9t8ZcIWEqQLByMCZEOJei6rW5N8khuXhDyMZaAChCmYkoodRKJuH9Aez9OGw:1uWWSp:D0GBrn668I8vh-j2P4t0Le3UJ7sBqcuPZ57BtpVPdyM', '2025-07-01 09:35:39.705646'),
('tnr4osksp79ofyaj7pn6091g0ehoiauw', '.eJxVjDsOwjAQRO_iGln-xllK-pzB2s3aOIBiKU4qxN1JpBRQTDPvzbxFxG0tcWtpiROLq-jF5bcjHJ9pPgA_cL5XOdZ5XSaShyJP2uRQOb1up_t3ULCVfZ0Mk1WegkPfMWogMCnrvIdNgKyNph7IggOfAzhUTCGZLqtRETkrPl_3pDg4:1ubIwI:nNB2fuRUpbY1WpkESo4evNNzug65n-PBufqEZNo2eRo', '2025-07-14 14:09:50.778134'),
('u8k353gxavn6jbbgkql4o2mgje80gu3a', '.eJxVjMsOgkAMRf9l1mYCFobWpXu-gbSdVlADCY-V8d-VhIVu7znnvkLH29p322JzN-RwCSmcfjdhfdi4g3zn8TZFncZ1HiTuSjzoEtsp2_N6uH8HPS_9t8ZcIWEqQLByMCZEOJei6rW5N8khuXhDyMZaAChCmYkoodRKJuH9Aez9OGw:1uWUUl:5sVGtE6fOireUA9V4hAO1yBWDMOQDHwXReEf23jzdX8', '2025-07-01 07:29:31.928239'),
('v0rdhf4gzuw2j614inoqay7t5q21p8ry', '.eJxVjMsOgkAMRf9l1mYCFobWpXu-gbSdVlADCY-V8d-VhIVu7znnvkLH29p322JzN-RwCSmcfjdhfdi4g3zn8TZFncZ1HiTuSjzoEtsp2_N6uH8HPS_9t8ZcIWEqQLByMCZEOJei6rW5N8khuXhDyMZaAChCmYkoodRKJuH9Aez9OGw:1uWHLS:aeSIqsURm2dtRYMB6dGP27G5VN4-3tbcKTbw_HpVme0', '2025-06-30 17:27:02.075357'),
('vwolf1m2sicnlplaco8pqsxlzybcxoii', '.eJxVjMsOgkAMRf9l1mYCFobWpXu-gbSdVlADCY-V8d-VhIVu7znnvkLH29p322JzN-RwCSmcfjdhfdi4g3zn8TZFncZ1HiTuSjzoEtsp2_N6uH8HPS_9t8ZcIWEqQLByMCZEOJei6rW5N8khuXhDyMZaAChCmYkoodRKJuH9Aez9OGw:1uWVR6:7Jj59xE-ReIpC0h1IENnpFR1zF9Rx3nIn8Y_U2bOa-g', '2025-07-01 08:29:48.628039'),
('ywnnt14fvo9mnev14303inucp91tnd3v', '.eJxVjMsOgkAMRf9l1mYCFobWpXu-gbSdVlADCY-V8d-VhIVu7znnvkLH29p322JzN-RwCSmcfjdhfdi4g3zn8TZFncZ1HiTuSjzoEtsp2_N6uH8HPS_9t8ZcIWEqQLByMCZEOJei6rW5N8khuXhDyMZaAChCmYkoodRKJuH9Aez9OGw:1uWLam:VpG7_17P4J-uhMtbR02_iVa9f_l9XECciqNw_wqmp5s', '2025-06-30 21:59:08.305338'),
('z00y9w135g7aeqo2cat0vwjp7s6o4apb', '.eJxVjMEOwiAQRP-FsyFAKbgevfsNzS67SNXQpLQn47_bJj3oYS7z3sxbDbguZVibzMPI6qKCOv12hOkpdQf8wHqfdJrqMo-kd0UftOnbxPK6Hu7fQcFWtrU4ps70FD32gdECgZNs8xZ2EbJ1ls5AHXjocwSPhimKC9kkQ-Q79fkC9nI4Ng:1ubxz0:qAhui8df-xQ54ZNHlqljy-EdqBBCd4AF_RrScbYNl4Q', '2025-07-16 09:59:22.401719'),
('zudkddcb6bmkpqphr03i7g7jjgopui3a', '.eJxVjMEOwiAQRP-FsyFAobgevfsNZJcFqRpISnsy_rtt0oMe5jLvzbxFwHUpYe1pDhOLiwBx-u0I4zPVHfAD673J2OoyTyR3RR60y1vj9Loe7t9BwV62dTJMg3LkLbqRUQOBSVnnLWw8ZG00nYEGsOCyB4uKySczZhUVkR3E5wv4PTg5:1uWZHq:cURqf2bFS5un5pDTKnEL_80bSWHzijJs7TmgW_ljCsk', '2025-07-01 12:36:30.808105');

-- --------------------------------------------------------

--
-- Table structure for table `grants_fund_allocation`
--

CREATE TABLE `grants_fund_allocation` (
  `id` bigint(20) NOT NULL,
  `allocation_id` char(32) NOT NULL,
  `allocation_type` varchar(20) NOT NULL,
  `allocated_amount` decimal(12,2) NOT NULL,
  `disbursed_amount` decimal(12,2) NOT NULL,
  `allocation_date` date NOT NULL,
  `disbursement_date` date DEFAULT NULL,
  `allocation_notes` longtext DEFAULT NULL,
  `disbursement_notes` longtext DEFAULT NULL,
  `ai_score` decimal(5,2) NOT NULL,
  `ai_factors` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`ai_factors`)),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `allocated_by_id` bigint(20) NOT NULL,
  `disbursed_by_id` bigint(20) DEFAULT NULL,
  `proposal_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `grants_grant_category`
--

CREATE TABLE `grants_grant_category` (
  `id` bigint(20) NOT NULL,
  `category_id` char(32) NOT NULL,
  `category_name` varchar(100) NOT NULL,
  `category_type` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `min_amount` decimal(12,2) NOT NULL,
  `max_amount` decimal(12,2) NOT NULL,
  `priority_weight` decimal(3,2) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `requires_approval` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `grants_grant_category`
--

INSERT INTO `grants_grant_category` (`id`, `category_id`, `category_name`, `category_type`, `description`, `min_amount`, `max_amount`, `priority_weight`, `is_active`, `requires_approval`, `created_at`, `updated_at`, `created_by_id`) VALUES
(1, 'd37ee21f64b14f5e8e75f0244b513854', 'Software deveopment', 'technology', 'This engages with grants that supports technology funds', 10000.00, 1000000.00, 0.90, 1, 1, '2025-06-30 13:17:59.458595', '2025-06-30 13:17:59.458595', 4),
(2, 'a90aef361887481bbdcf6d290022cbbf', 'Electronics', 'technology', 'For hardware devices grants', 100000.00, 999999.99, 1.00, 1, 1, '2025-06-30 13:24:34.341043', '2025-06-30 13:24:34.341043', NULL),
(4, '119fdf7ff243436b9945c988072884cc', 'Academic', 'academic', 'Academic programs and support', 500000.00, 5000000.00, 0.80, 1, 1, '2025-06-30 13:26:35.172077', '2025-06-30 13:36:29.603140', 6),
(5, '2f7c15c6a9f84cc1b308df33a84d23a5', 'Technology', 'technology', 'Technology and ICT grants', 200000.00, 2000000.00, 0.90, 1, 1, '2025-06-30 13:26:35.173103', '2025-06-30 13:26:35.173103', 6),
(6, '76a506875a0f46cda2babf445c3f3c9c', 'Education', 'other', 'Education grants', 0.00, 0.00, 1.00, 1, 1, '2025-07-01 09:04:53.391557', '2025-07-01 09:04:53.391557', NULL),
(7, 'ff04b5b86e5e40eb8670656ece43768f', 'Mobile applications', 'sports', 'Develop mobile applications', 120000.00, 240000.00, 8.89, 1, 1, '2025-07-02 11:44:46.567187', '2025-07-02 11:44:46.567187', 13);

-- --------------------------------------------------------

--
-- Table structure for table `grants_grant_proposal`
--

CREATE TABLE `grants_grant_proposal` (
  `id` bigint(20) NOT NULL,
  `proposal_id` char(32) NOT NULL,
  `proposal_title` varchar(200) NOT NULL,
  `proposal_code` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `objectives` longtext NOT NULL,
  `expected_outcomes` longtext NOT NULL,
  `target_beneficiaries` longtext NOT NULL,
  `requested_amount` decimal(12,2) NOT NULL,
  `allocated_amount` decimal(12,2) NOT NULL,
  `disbursed_amount` decimal(12,2) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `priority_level` varchar(10) NOT NULL,
  `status` varchar(20) NOT NULL,
  `submission_date` datetime(6) DEFAULT NULL,
  `approval_date` datetime(6) DEFAULT NULL,
  `completion_date` datetime(6) DEFAULT NULL,
  `review_notes` longtext DEFAULT NULL,
  `rejection_reason` longtext DEFAULT NULL,
  `ai_priority_score` decimal(5,2) NOT NULL,
  `ai_need_score` decimal(5,2) NOT NULL,
  `ai_impact_score` decimal(5,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_by_id` bigint(20) DEFAULT NULL,
  `created_by_id` bigint(20) NOT NULL,
  `grant_category_id` bigint(20) NOT NULL,
  `school_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `grants_grant_proposal`
--

INSERT INTO `grants_grant_proposal` (`id`, `proposal_id`, `proposal_title`, `proposal_code`, `description`, `objectives`, `expected_outcomes`, `target_beneficiaries`, `requested_amount`, `allocated_amount`, `disbursed_amount`, `start_date`, `end_date`, `priority_level`, `status`, `submission_date`, `approval_date`, `completion_date`, `review_notes`, `rejection_reason`, `ai_priority_score`, `ai_need_score`, `ai_impact_score`, `created_at`, `updated_at`, `approved_by_id`, `created_by_id`, `grant_category_id`, `school_id`) VALUES
(2, '82e4de5b0e844c57a48d13cce78e4315', 'Ehaho', 'GP2025060002', 'for online buying..', 'removed cost of transoprot', 'reduces cost of living', 'urban people..', 1000000.00, 0.00, 0.00, '2025-06-30', '2026-06-30', 'high', 'rejected', NULL, '2025-06-30 14:59:13.154304', NULL, NULL, 'not full', 0.00, 0.00, 0.00, '2025-06-30 14:02:05.894343', '2025-06-30 14:59:32.119635', NULL, 6, 2, 1),
(3, 'd62165ab29c847fc932de959f684ac3a', 'Grant Proposal Kigali 1', 'GP2025070003', 'Dummy proposal for Kigali', '', '', '', 1000000.00, 0.00, 0.00, '2025-05-02', '2025-08-30', 'medium', 'approved', NULL, '2025-07-01 09:04:53.396249', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.401255', '2025-07-01 09:04:53.401255', NULL, 10, 6, 4),
(4, '73f5c530bd4d40a78fe79c6940cb35e3', 'Grant Proposal Kigali 2', 'GP2025070004', 'Dummy proposal for Kigali', '', '', '', 2000000.00, 0.00, 0.00, '2025-05-02', '2025-08-30', 'medium', 'approved', NULL, '2025-06-01 09:04:53.405250', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.407248', '2025-07-01 09:04:53.407248', NULL, 10, 6, 4),
(5, '40360b6d41d44268b31f72d3cfc175a8', 'Grant Proposal Kigali 3', 'GP2025070005', 'Dummy proposal for Kigali', '', '', '', 3000000.00, 0.00, 0.00, '2025-05-02', '2025-08-30', 'medium', 'approved', NULL, '2025-05-02 09:04:53.409600', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.410605', '2025-07-01 09:04:53.410605', NULL, 10, 6, 4),
(6, 'a990f50f35f84b6eafe8afaa27796432', 'Grant Proposal Eastern 1', 'GP2025070006', 'Dummy proposal for Eastern', '', '', '', 2000000.00, 0.00, 0.00, '2025-05-02', '2025-08-30', 'medium', 'approved', NULL, '2025-07-01 09:04:53.414416', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.415390', '2025-07-01 09:04:53.415390', NULL, 10, 6, 5),
(7, '7b04c30e41134fbd8902dadd9cd047af', 'Grant Proposal Eastern 2', 'GP2025070007', 'Dummy proposal for Eastern', '', '', '', 4000000.00, 0.00, 0.00, '2025-05-02', '2025-08-30', 'medium', 'approved', NULL, '2025-06-01 09:04:53.418612', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.419635', '2025-07-01 09:04:53.419635', NULL, 10, 6, 5),
(8, '480a50786a1b4499a6782562f2e1e27a', 'Grant Proposal Eastern 3', 'GP2025070008', 'Dummy proposal for Eastern', '', '', '', 6000000.00, 0.00, 0.00, '2025-05-02', '2025-08-30', 'medium', 'approved', NULL, '2025-05-02 09:04:53.421613', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.422613', '2025-07-01 09:04:53.422613', NULL, 10, 6, 5),
(9, '8671bc70e6e643c2a2b7cdfb65185fff', 'Grant Proposal Western 1', 'GP2025070009', 'Dummy proposal for Western', '', '', '', 3000000.00, 0.00, 0.00, '2025-05-02', '2025-08-30', 'medium', 'approved', NULL, '2025-07-01 09:04:53.425613', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.426613', '2025-07-01 09:04:53.426613', NULL, 10, 6, 6),
(10, 'ef806f04d69f45b9a94b0a33ca8d6d71', 'Grant Proposal Western 2', 'GP2025070010', 'Dummy proposal for Western', '', '', '', 6000000.00, 0.00, 0.00, '2025-05-02', '2025-08-30', 'medium', 'approved', NULL, '2025-06-01 09:04:53.428847', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.428847', '2025-07-01 09:04:53.428847', NULL, 10, 6, 6),
(11, 'b63cf102645b405e90d754950308892d', 'Grant Proposal Western 3', 'GP2025070011', 'Dummy proposal for Western', '', '', '', 9000000.00, 0.00, 0.00, '2025-05-02', '2025-08-30', 'medium', 'approved', NULL, '2025-05-02 09:04:53.431226', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.432244', '2025-07-01 09:04:53.432244', NULL, 10, 6, 6),
(12, 'f5f071199a7f44fdaa0982a8609b0bcc', 'Grant Proposal Southern 1', 'GP2025070012', 'Dummy proposal for Southern', '', '', '', 4000000.00, 0.00, 0.00, '2025-05-02', '2025-08-30', 'medium', 'approved', NULL, '2025-07-01 09:04:53.438243', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.439352', '2025-07-01 09:04:53.439352', NULL, 10, 6, 7),
(13, '6e759154841e4446b66c5510a554cdd6', 'Grant Proposal Southern 2', 'GP2025070013', 'Dummy proposal for Southern', '', '', '', 8000000.00, 0.00, 0.00, '2025-05-02', '2025-08-30', 'medium', 'approved', NULL, '2025-06-01 09:04:53.441353', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.442354', '2025-07-01 09:04:53.442354', NULL, 10, 6, 7),
(14, 'b7d35f09416d48558553a475d4a87ab9', 'Grant Proposal Southern 3', 'GP2025070014', 'Dummy proposal for Southern', '', '', '', 12000000.00, 0.00, 0.00, '2025-05-02', '2025-08-30', 'medium', 'approved', NULL, '2025-05-02 09:04:53.447369', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.449443', '2025-07-01 09:04:53.449443', NULL, 10, 6, 7),
(15, '3c8591288e80491997246fd8b97e8fa9', 'Grant Proposal Northern 1', 'GP2025070015', 'Dummy proposal for Northern', 'ikejnv', 'ugiejfm', 'uigehifhhcb', 5000000.00, 0.00, 0.00, '2025-05-02', '2025-08-30', 'medium', 'submitted', NULL, '2025-07-01 09:04:53.453834', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.454948', '2025-07-15 17:56:15.995260', NULL, 10, 6, 8),
(16, '5cd6ac967cea4f75b36b73e7e27036ff', 'Grant Proposal Northern 2', 'GP2025070016', 'Dummy proposal for Northern', '', '', '', 10000000.00, 25000.00, 0.00, '2025-05-02', '2025-08-30', 'medium', 'funded', NULL, '2025-06-01 09:04:53.456875', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.457953', '2025-07-01 10:57:21.519867', NULL, 10, 6, 8),
(17, '34d236730e734806a239c29931beb117', 'Grant Proposal Northern 3', 'GP2025070017', 'This project will engage with helping people get jobs', 'Hire many people', '50% people get jobs', 'Undergraduates and graduates unemployed', 15000000.00, 0.00, 0.00, '2025-05-02', '2025-08-30', 'medium', 'funded', NULL, '2025-05-02 09:04:53.459060', NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-01 09:04:53.461062', '2025-07-15 17:53:15.911627', NULL, 10, 6, 8),
(18, 'dea8aa96b97f49f29d96edb87775a37a', 'Enhancing ICT Infrastructure for Digital Learning', 'GP2025070018', 'werth', 'fghjk', 'fghjk', 'fghjk', 2000000.00, 0.00, 0.00, '2025-07-16', '2026-07-16', 'medium', 'submitted', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, '2025-07-16 08:39:57.450931', '2025-07-16 08:39:57.450931', NULL, 6, 6, 5);

-- --------------------------------------------------------

--
-- Table structure for table `grants_proposal_budget`
--

CREATE TABLE `grants_proposal_budget` (
  `id` bigint(20) NOT NULL,
  `budget_id` char(32) NOT NULL,
  `item_category` varchar(20) NOT NULL,
  `item_description` varchar(200) NOT NULL,
  `quantity` int(10) UNSIGNED NOT NULL CHECK (`quantity` >= 0),
  `unit_cost` decimal(10,2) NOT NULL,
  `total_cost` decimal(12,2) NOT NULL,
  `allocated_amount` decimal(12,2) NOT NULL,
  `spent_amount` decimal(12,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) NOT NULL,
  `proposal_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `grants_proposal_document`
--

CREATE TABLE `grants_proposal_document` (
  `id` bigint(20) NOT NULL,
  `document_id` char(32) NOT NULL,
  `document_type` varchar(20) NOT NULL,
  `document_title` varchar(200) NOT NULL,
  `document_file` varchar(100) NOT NULL,
  `file_size` int(10) UNSIGNED NOT NULL CHECK (`file_size` >= 0),
  `description` longtext DEFAULT NULL,
  `is_required` tinyint(1) NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `proposal_id` bigint(20) NOT NULL,
  `uploaded_by_id` bigint(20) NOT NULL,
  `ocr_text` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `grants_proposal_review`
--

CREATE TABLE `grants_proposal_review` (
  `id` bigint(20) NOT NULL,
  `review_id` char(32) NOT NULL,
  `review_status` varchar(20) NOT NULL,
  `review_notes` longtext NOT NULL,
  `technical_score` decimal(5,2) NOT NULL,
  `feasibility_score` decimal(5,2) NOT NULL,
  `impact_score` decimal(5,2) NOT NULL,
  `review_start_date` datetime(6) NOT NULL,
  `review_completion_date` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `proposal_id` bigint(20) NOT NULL,
  `reviewer_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `procurement_bid`
--

CREATE TABLE `procurement_bid` (
  `id` bigint(20) NOT NULL,
  `bid_id` char(32) NOT NULL,
  `proposal_text` longtext NOT NULL,
  `document` varchar(100) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `submitted_at` datetime(6) NOT NULL,
  `reviewed_at` datetime(6) DEFAULT NULL,
  `awarded_at` datetime(6) DEFAULT NULL,
  `supplier_id` bigint(20) NOT NULL,
  `tender_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `procurement_bid`
--

INSERT INTO `procurement_bid` (`id`, `bid_id`, `proposal_text`, `document`, `status`, `submitted_at`, `reviewed_at`, `awarded_at`, `supplier_id`, `tender_id`) VALUES
(1, '54269ee6ad914f35bbddd44ae51233a5', 'I\'m tender', 'bid_documents/financial_report.pdf', 'awarded', '2025-07-15 18:24:43.148880', NULL, '2025-07-15 18:24:52.720941', 17, 1),
(2, '68429e711ba2450296552d6d7564e27b', 'Hod josb  ehiog j', 'bid_documents/performance_report.pdf', 'submitted', '2025-07-16 08:58:30.110882', NULL, NULL, 18, 2);

-- --------------------------------------------------------

--
-- Table structure for table `procurement_tender`
--

CREATE TABLE `procurement_tender` (
  `id` bigint(20) NOT NULL,
  `tender_id` char(32) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `published_at` datetime(6) DEFAULT NULL,
  `submission_deadline` datetime(6) NOT NULL,
  `awarded_to` varchar(200) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL,
  `school_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `procurement_tender`
--

INSERT INTO `procurement_tender` (`id`, `tender_id`, `title`, `description`, `status`, `published_at`, `submission_deadline`, `awarded_to`, `created_at`, `updated_at`, `created_by_id`, `school_id`) VALUES
(1, '0783a8be46004dee8262b0076a7a0d7d', 'Hanz', 'jhiuiajne9', 'awarded', NULL, '2025-07-14 05:04:00.000000', 'DUSABIMANA Hozana', '2025-07-14 05:01:22.201663', '2025-07-15 18:24:52.739088', 6, 5),
(2, '1d91babdefab4901aacd3121490eea10', 'Laptop deliver', 'to give students laptops', 'open', NULL, '2025-07-16 08:47:00.000000', NULL, '2025-07-16 08:45:32.934824', '2025-07-16 08:45:32.934824', 6, 4);

-- --------------------------------------------------------

--
-- Table structure for table `procurement_tenderdocument`
--

CREATE TABLE `procurement_tenderdocument` (
  `id` bigint(20) NOT NULL,
  `document_id` char(32) NOT NULL,
  `document_type` varchar(20) NOT NULL,
  `document_title` varchar(200) NOT NULL,
  `document_file` varchar(100) NOT NULL,
  `file_size` int(10) UNSIGNED NOT NULL CHECK (`file_size` >= 0),
  `description` longtext DEFAULT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `ocr_text` longtext DEFAULT NULL,
  `tender_id` bigint(20) NOT NULL,
  `uploaded_by_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `procurement_tenderstatushistory`
--

CREATE TABLE `procurement_tenderstatushistory` (
  `id` bigint(20) NOT NULL,
  `old_status` varchar(20) NOT NULL,
  `new_status` varchar(20) NOT NULL,
  `changed_at` datetime(6) NOT NULL,
  `changed_by_id` bigint(20) DEFAULT NULL,
  `tender_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reporting_analytics_event`
--

CREATE TABLE `reporting_analytics_event` (
  `id` bigint(20) NOT NULL,
  `event_id` char(32) NOT NULL,
  `event_type` varchar(20) NOT NULL,
  `event_name` varchar(200) NOT NULL,
  `session_id` varchar(100) DEFAULT NULL,
  `page_url` varchar(200) DEFAULT NULL,
  `referrer_url` varchar(200) DEFAULT NULL,
  `user_agent` longtext DEFAULT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `event_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`event_data`)),
  `metadata` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`metadata`)),
  `timestamp` datetime(6) NOT NULL,
  `duration_seconds` int(10) UNSIGNED NOT NULL CHECK (`duration_seconds` >= 0),
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reporting_analytics_event`
--

INSERT INTO `reporting_analytics_event` (`id`, `event_id`, `event_type`, `event_name`, `session_id`, `page_url`, `referrer_url`, `user_agent`, `ip_address`, `event_data`, `metadata`, `timestamp`, `duration_seconds`, `user_id`) VALUES
(1, '5a486b9ca4084429ad7b7251846d1c1a', 'report_generate', 'Dummy Event 1', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:32:00.567560', 0, 10),
(2, 'dd3b70ab623845c18febd893ad35947f', 'report_generate', 'Dummy Event 2', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:32:00.571712', 0, 10),
(3, 'aa7eafdbccf84041a521249fe41f6cf7', 'button_click', 'Dummy Event 3', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:32:00.573789', 0, 10),
(4, '66d2d13fb1d44bdfb85305884699f61f', 'page_view', 'Dummy Event 4', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:32:00.575801', 0, 10),
(5, 'c718043e45564501ad15c8336bfbc2c5', 'report_generate', 'Dummy Event 5', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:32:00.577801', 0, 10),
(6, '97997219da6b47b684b74de50146a79a', 'button_click', 'Dummy Event 6', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:32:00.579934', 0, 10),
(7, 'f87eabb9c54044ada8cf00de59ae9ca8', 'report_generate', 'Dummy Event 7', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:32:00.581949', 0, 10),
(8, 'f2a732d53d3a48bb9e5fd749338cdaff', 'button_click', 'Dummy Event 8', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:32:00.584180', 0, 10),
(9, '0b4a79783e9641c68a522924d8714b1a', 'report_generate', 'Dummy Event 9', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:32:00.587206', 0, 10),
(10, 'c30a9e7feba045d0a0b89a09eb005098', 'page_view', 'Dummy Event 10', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:32:00.589999', 0, 10),
(11, '461e5812f101436fb5b5143026900ce3', 'button_click', 'Dummy Event 1', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:34:02.012280', 0, 10),
(12, '598852945a05475db4cf8456342dcc21', 'page_view', 'Dummy Event 2', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:34:02.015798', 0, 10),
(13, 'cbe83ebd28ae4a73bc4894b5d85680f5', 'page_view', 'Dummy Event 3', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:34:02.018001', 0, 10),
(14, '3bcea28d7f8943a486479fb5b5fd6c43', 'button_click', 'Dummy Event 4', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:34:02.023109', 0, 10),
(15, '235f10656ea04a2c96a374c8e4542209', 'page_view', 'Dummy Event 6', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:34:02.026117', 0, 10),
(16, '37750657256e4ab4a94ad745f66443e2', 'button_click', 'Dummy Event 7', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:34:02.028254', 0, 10),
(17, 'dd6a54602cf24da09e203a1ca7bff40c', 'button_click', 'Dummy Event 10', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:34:02.032256', 0, 10),
(18, '2b052239eede4a6dbb35df1a63f07d15', 'page_view', 'Dummy Event 1', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:34:30.075392', 0, 10),
(19, '5652520c7cb24769be508c1c67dffd46', 'button_click', 'Dummy Event 2', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:34:30.078896', 0, 10),
(20, 'a24c5f11f12d42e2b4f315ed2ed8ab90', 'button_click', 'Dummy Event 5', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:34:30.082016', 0, 10),
(21, 'e907fa3822ad4f34ab78b3cbd589b52f', 'report_generate', 'Dummy Event 6', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:34:30.085015', 0, 10),
(22, 'bf86e3fe24fa4c37942d2b94134b1492', 'report_generate', 'Dummy Event 8', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:34:30.088017', 0, 10),
(23, '0677e3b3838b490cb087ed2563388560', 'page_view', 'Dummy Event 9', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 08:34:30.091476', 0, 10),
(24, 'aea6eb835200479e8af9d0b1c162c704', 'report_generate', 'Dummy Event 3', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 09:04:53.508539', 0, 10),
(25, '8832ec93a0a34dd1b0468bbda6a7e49b', 'report_generate', 'Dummy Event 4', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 09:04:53.512747', 0, 10),
(26, 'f8d9ee81440742d18ad43c0064e59395', 'page_view', 'Dummy Event 8', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 09:04:53.518896', 0, 10),
(27, 'd8a532b48ae2403fb28c5013292d3122', 'report_generate', 'Dummy Event 10', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 09:04:53.522240', 0, 10),
(28, 'ca7a7c69b8d04984b7fd881f8b3674e5', 'button_click', 'Dummy Event 9', NULL, NULL, NULL, NULL, NULL, '{}', '{}', '2025-07-01 10:45:24.106479', 0, 10);

-- --------------------------------------------------------

--
-- Table structure for table `reporting_dashboard`
--

CREATE TABLE `reporting_dashboard` (
  `id` bigint(20) NOT NULL,
  `dashboard_id` char(32) NOT NULL,
  `dashboard_name` varchar(200) NOT NULL,
  `dashboard_type` varchar(20) NOT NULL,
  `description` longtext DEFAULT NULL,
  `layout_config` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`layout_config`)),
  `is_default` tinyint(1) NOT NULL,
  `is_public` tinyint(1) NOT NULL,
  `refresh_interval` int(10) UNSIGNED NOT NULL CHECK (`refresh_interval` >= 0),
  `is_active` tinyint(1) NOT NULL,
  `last_accessed` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `school_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reporting_dashboard_widget`
--

CREATE TABLE `reporting_dashboard_widget` (
  `id` bigint(20) NOT NULL,
  `widget_id` char(32) NOT NULL,
  `widget_name` varchar(200) NOT NULL,
  `widget_type` varchar(20) NOT NULL,
  `chart_type` varchar(20) DEFAULT NULL,
  `data_source` varchar(100) NOT NULL,
  `configuration` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`configuration`)),
  `position_x` int(10) UNSIGNED NOT NULL CHECK (`position_x` >= 0),
  `position_y` int(10) UNSIGNED NOT NULL CHECK (`position_y` >= 0),
  `width` int(10) UNSIGNED NOT NULL CHECK (`width` >= 0),
  `height` int(10) UNSIGNED NOT NULL CHECK (`height` >= 0),
  `is_visible` tinyint(1) NOT NULL,
  `auto_refresh` tinyint(1) NOT NULL,
  `refresh_interval` int(10) UNSIGNED NOT NULL CHECK (`refresh_interval` >= 0),
  `last_data_update` datetime(6) DEFAULT NULL,
  `cached_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`cached_data`)),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `dashboard_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reporting_data_export`
--

CREATE TABLE `reporting_data_export` (
  `id` bigint(20) NOT NULL,
  `export_id` char(32) NOT NULL,
  `export_type` varchar(20) NOT NULL,
  `format` varchar(10) NOT NULL,
  `description` longtext DEFAULT NULL,
  `filters` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`filters`)),
  `export_file` varchar(100) DEFAULT NULL,
  `file_size` int(10) UNSIGNED NOT NULL CHECK (`file_size` >= 0),
  `status` varchar(20) NOT NULL,
  `row_count` int(10) UNSIGNED NOT NULL CHECK (`row_count` >= 0),
  `processing_time_seconds` int(10) UNSIGNED NOT NULL CHECK (`processing_time_seconds` >= 0),
  `error_message` longtext DEFAULT NULL,
  `download_count` int(10) UNSIGNED NOT NULL CHECK (`download_count` >= 0),
  `last_downloaded` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `completed_at` datetime(6) DEFAULT NULL,
  `school_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reporting_data_export`
--

INSERT INTO `reporting_data_export` (`id`, `export_id`, `export_type`, `format`, `description`, `filters`, `export_file`, `file_size`, `status`, `row_count`, `processing_time_seconds`, `error_message`, `download_count`, `last_downloaded`, `created_at`, `completed_at`, `school_id`, `user_id`) VALUES
(1, '809453c0cd1e4f11a91a26614e186838', 'users', 'csv', 'Dummy export', '{}', '', 0, 'completed', 83, 10, NULL, 3, NULL, '2025-07-01 08:32:00.595999', NULL, NULL, 10),
(2, '786701a0699b4ea892b0ef2d44550aa9', 'grants', 'pdf', 'Dummy export', '{}', '', 0, 'completed', 52, 4, NULL, 10, NULL, '2025-07-01 08:32:00.598999', NULL, NULL, 10),
(3, '3a07eeb3213a455e89282b4db2c5bed5', 'users', 'excel', 'Dummy export', '{}', '', 0, 'completed', 81, 5, NULL, 5, NULL, '2025-07-01 08:32:00.601113', NULL, NULL, 10),
(4, 'f0bd0c6560d2431692b6816df25026cb', 'budgets', 'pdf', 'Dummy export', '{}', '', 0, 'completed', 23, 4, NULL, 1, NULL, '2025-07-01 08:32:00.603763', NULL, NULL, 10),
(5, 'd8eb6ba1a89a4e61b786bbd37f5fb2bd', 'grants', 'excel', 'Dummy export', '{}', '', 0, 'completed', 92, 10, NULL, 7, NULL, '2025-07-01 08:34:02.034346', NULL, NULL, 10),
(6, '9295f0162fcb40759a2db701d9d909d3', 'schools', 'excel', 'Dummy export', '{}', '', 0, 'completed', 37, 7, NULL, 6, NULL, '2025-07-01 08:34:02.036850', NULL, NULL, 10),
(7, '3a8323706e24456caba77648b0b78939', 'schools', 'csv', 'Dummy export', '{}', '', 0, 'completed', 16, 1, NULL, 7, NULL, '2025-07-01 08:34:02.041375', NULL, NULL, 10),
(8, '3af01a397e9d464a98d12a4df8842850', 'budgets', 'csv', 'Dummy export', '{}', '', 0, 'completed', 92, 5, NULL, 1, NULL, '2025-07-01 08:34:30.094274', NULL, NULL, 10),
(9, '44db6f492eb44ccc80cd06f761031ad8', 'schools', 'pdf', 'Dummy export', '{}', '', 0, 'completed', 53, 5, NULL, 10, NULL, '2025-07-01 08:34:30.097278', NULL, NULL, 10),
(10, 'c2329008b2094edcb18a0893e5853e7d', 'reports', 'excel', 'Dummy export', '{}', '', 0, 'completed', 42, 6, NULL, 6, NULL, '2025-07-01 09:04:53.524241', NULL, NULL, 10),
(11, '176152cdd0844a0e92926d0d0257503d', 'reports', 'csv', 'Dummy export', '{}', '', 0, 'completed', 94, 4, NULL, 5, NULL, '2025-07-01 10:45:24.110872', NULL, NULL, 10),
(12, '87c4268b84934c86a9e09661d2f301bb', 'budgets', 'excel', 'Dummy export', '{}', '', 0, 'completed', 12, 10, NULL, 7, NULL, '2025-07-01 10:45:24.115872', NULL, NULL, 10);

-- --------------------------------------------------------

--
-- Table structure for table `reporting_kpi`
--

CREATE TABLE `reporting_kpi` (
  `id` bigint(20) NOT NULL,
  `kpi_id` char(32) NOT NULL,
  `kpi_name` varchar(200) NOT NULL,
  `kpi_category` varchar(20) NOT NULL,
  `kpi_type` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `calculation_formula` longtext NOT NULL,
  `unit_of_measure` varchar(50) DEFAULT NULL,
  `target_value` decimal(15,4) NOT NULL,
  `threshold_value` decimal(15,4) NOT NULL,
  `min_value` decimal(15,4) NOT NULL,
  `max_value` decimal(15,4) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_system` tinyint(1) NOT NULL,
  `auto_calculate` tinyint(1) NOT NULL,
  `applicable_roles` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`applicable_roles`)),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reporting_kpi`
--

INSERT INTO `reporting_kpi` (`id`, `kpi_id`, `kpi_name`, `kpi_category`, `kpi_type`, `description`, `calculation_formula`, `unit_of_measure`, `target_value`, `threshold_value`, `min_value`, `max_value`, `is_active`, `is_system`, `auto_calculate`, `applicable_roles`, `created_at`, `updated_at`, `created_by_id`) VALUES
(1, '04f0d04b099e42abb03963dfd1f5780c', 'Dummy KPI 1', 'academic', 'percentage', 'Description for KPI 1', 'Random formula', 'units', 100.0000, 80.0000, 0.0000, 200.0000, 1, 0, 1, '[\"reb_officer\", \"school_admin\"]', '2025-07-01 08:32:00.372538', '2025-07-01 08:32:00.372538', 10),
(2, '12910528a0d643dca3e77a5321d0af9f', 'Dummy KPI 2', 'operational', 'currency', 'Description for KPI 2', 'Random formula', 'units', 100.0000, 80.0000, 0.0000, 200.0000, 1, 0, 1, '[\"reb_officer\", \"school_admin\"]', '2025-07-01 08:32:00.375544', '2025-07-01 08:32:00.375544', 10),
(3, '037a3fca40e34a0abb3d9e8bdee1e384', 'Dummy KPI 3', 'academic', 'currency', 'Description for KPI 3', 'Random formula', 'units', 100.0000, 80.0000, 0.0000, 200.0000, 1, 0, 1, '[\"reb_officer\", \"school_admin\"]', '2025-07-01 08:32:00.378098', '2025-07-01 08:32:00.378098', 10),
(4, 'e2d9cd48ad79477694e3c06b1af9f943', 'Dummy KPI 4', 'financial', 'count', 'Description for KPI 4', 'Random formula', 'units', 100.0000, 80.0000, 0.0000, 200.0000, 1, 0, 1, '[\"reb_officer\", \"school_admin\"]', '2025-07-01 08:32:00.379824', '2025-07-01 08:32:00.379824', 10),
(5, '09010dab506949399677a4f17140eda2', 'Dummy KPI 5', 'financial', 'currency', 'Description for KPI 5', 'Random formula', 'units', 100.0000, 80.0000, 0.0000, 200.0000, 1, 0, 1, '[\"reb_officer\", \"school_admin\"]', '2025-07-01 08:32:00.382590', '2025-07-01 08:32:00.382590', 10);

-- --------------------------------------------------------

--
-- Table structure for table `reporting_kpi_value`
--

CREATE TABLE `reporting_kpi_value` (
  `id` bigint(20) NOT NULL,
  `value_id` char(32) NOT NULL,
  `value` decimal(15,4) NOT NULL,
  `measurement_date` date NOT NULL,
  `measurement_period` varchar(50) NOT NULL,
  `context_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`context_data`)),
  `is_above_target` tinyint(1) NOT NULL,
  `is_above_threshold` tinyint(1) NOT NULL,
  `performance_status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `calculated_by_id` bigint(20) DEFAULT NULL,
  `kpi_id` bigint(20) NOT NULL,
  `school_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reporting_kpi_value`
--

INSERT INTO `reporting_kpi_value` (`id`, `value_id`, `value`, `measurement_date`, `measurement_period`, `context_data`, `is_above_target`, `is_above_threshold`, `performance_status`, `created_at`, `calculated_by_id`, `kpi_id`, `school_id`) VALUES
(1, 'f2eb7927049a4dcbb805883d576e2562', 143.5536, '2025-07-01', 'Monthly', '{}', 0, 1, 'good', '2025-07-01 08:32:00.392476', 10, 1, 3),
(2, '276068654b284182a976d077230cc005', 61.3861, '2025-06-01', 'Monthly', '{}', 0, 0, 'excellent', '2025-07-01 08:32:00.395479', 10, 1, 3),
(3, '98e7cfc2ddef4bfaa2b1eb2972a98a56', 53.4656, '2025-05-02', 'Monthly', '{}', 1, 0, 'good', '2025-07-01 08:32:00.398718', 10, 1, 3),
(4, 'e5602c403f7544ef93116ec607c4e7dd', 77.0544, '2025-04-02', 'Monthly', '{}', 1, 1, 'good', '2025-07-01 08:32:00.400942', 10, 1, 3),
(5, '29721131f9f74091b3613e7a328ec7a8', 62.1153, '2025-03-03', 'Monthly', '{}', 1, 1, 'excellent', '2025-07-01 08:32:00.404936', 10, 1, 3),
(6, '848d89515dda47559135890ad6910497', 75.2574, '2025-02-01', 'Monthly', '{}', 0, 0, 'excellent', '2025-07-01 08:32:00.407936', 10, 1, 3),
(7, 'f5f2d13f0d324fd28e5b0d3453cdad95', 147.4764, '2025-07-01', 'Monthly', '{}', 1, 1, 'fair', '2025-07-01 08:32:00.410063', 10, 2, 3),
(8, 'bf700eca1ec941ba9ccd9ec277925abb', 61.6490, '2025-06-01', 'Monthly', '{}', 0, 0, 'poor', '2025-07-01 08:32:00.412040', 10, 2, 3),
(9, '0e84990e06d0404b9dfb8edf47b006c1', 111.3568, '2025-05-02', 'Monthly', '{}', 1, 1, 'good', '2025-07-01 08:32:00.415038', 10, 2, 3),
(10, '6ed4ae314bff4765938600376e2f6aef', 144.4943, '2025-04-02', 'Monthly', '{}', 0, 0, 'excellent', '2025-07-01 08:32:00.416228', 10, 2, 3),
(11, 'c2f2f90aa7414343b6c9a1a197357c7f', 64.9024, '2025-03-03', 'Monthly', '{}', 0, 0, 'fair', '2025-07-01 08:32:00.419385', 10, 2, 3),
(12, '84be5b787fa14c639b1d48b102e8e0a4', 66.9763, '2025-02-01', 'Monthly', '{}', 1, 0, 'fair', '2025-07-01 08:32:00.423225', 10, 2, 3),
(13, '6f80b0b07d7b45a0a3f2dfbb95b8c7cb', 59.4893, '2025-07-01', 'Monthly', '{}', 1, 0, 'critical', '2025-07-01 08:32:00.445927', 10, 3, 3),
(14, 'dae1d4fd45624dabb2e655eb2598eab7', 142.0886, '2025-06-01', 'Monthly', '{}', 1, 1, 'fair', '2025-07-01 08:32:00.448922', 10, 3, 3),
(15, '4f759739821945a59cd27cfc712ed020', 108.3148, '2025-05-02', 'Monthly', '{}', 0, 1, 'critical', '2025-07-01 08:32:00.451337', 10, 3, 3),
(16, '4b8bd7b559f7489595e9b09fb28a33e6', 51.2840, '2025-04-02', 'Monthly', '{}', 1, 0, 'fair', '2025-07-01 08:32:00.454851', 10, 3, 3),
(17, '26b2ce839e76460bb69d7a0e035c350d', 113.3938, '2025-03-03', 'Monthly', '{}', 1, 0, 'fair', '2025-07-01 08:32:00.457884', 10, 3, 3),
(18, '4b4233a6129a4dccb4a010095a521a27', 110.1211, '2025-02-01', 'Monthly', '{}', 1, 0, 'good', '2025-07-01 08:32:00.461048', 10, 3, 3),
(19, 'ce0c985dc3684d4a96f34fdda93d2b5e', 71.3358, '2025-07-01', 'Monthly', '{}', 0, 0, 'excellent', '2025-07-01 08:32:00.463047', 10, 4, 3),
(20, 'a25255a16b584e4ca759335ab88b11fe', 107.1885, '2025-06-01', 'Monthly', '{}', 1, 1, 'poor', '2025-07-01 08:32:00.465048', 10, 4, 3),
(21, 'f651365e775a4133b51f1d2e2c77ac05', 81.6855, '2025-05-02', 'Monthly', '{}', 0, 0, 'poor', '2025-07-01 08:32:00.467049', 10, 4, 3),
(22, '4ca975366d2545a1bd6a328b2c154bcc', 55.9401, '2025-04-02', 'Monthly', '{}', 0, 1, 'fair', '2025-07-01 08:32:00.469139', 10, 4, 3),
(23, '336814de560046c49930fdd36e4a3ed8', 98.6351, '2025-03-03', 'Monthly', '{}', 0, 1, 'fair', '2025-07-01 08:32:00.473706', 10, 4, 3),
(24, '6054f6a398934af698f599f3060dc1f2', 53.8230, '2025-02-01', 'Monthly', '{}', 0, 1, 'poor', '2025-07-01 08:32:00.475706', 10, 4, 3),
(25, '07c2c4786ab84a10be69b7718ed6ab23', 60.8678, '2025-07-01', 'Monthly', '{}', 1, 1, 'critical', '2025-07-01 08:32:00.477993', 10, 5, 3),
(26, 'c876347136414b1ca6ef588145bd244b', 83.2438, '2025-06-01', 'Monthly', '{}', 1, 0, 'fair', '2025-07-01 08:32:00.480118', 10, 5, 3),
(27, '632712013c4a4f60a6b64b18b8ff503e', 106.7736, '2025-05-02', 'Monthly', '{}', 1, 0, 'excellent', '2025-07-01 08:32:00.482118', 10, 5, 3),
(28, '409aef0ade46404dab1245713f686144', 80.5121, '2025-04-02', 'Monthly', '{}', 0, 1, 'fair', '2025-07-01 08:32:00.484119', 10, 5, 3),
(29, '379c6b4b45de4ad0bbe794b4c0d4c711', 72.7517, '2025-03-03', 'Monthly', '{}', 0, 1, 'poor', '2025-07-01 08:32:00.489122', 10, 5, 3),
(30, '4a67b54a084c4a6d913709312630e036', 142.5454, '2025-02-01', 'Monthly', '{}', 1, 0, 'good', '2025-07-01 08:32:00.492118', 10, 5, 3);

-- --------------------------------------------------------

--
-- Table structure for table `reporting_proposal_criterion`
--

CREATE TABLE `reporting_proposal_criterion` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `type` varchar(10) NOT NULL,
  `required` tinyint(1) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `ordering` int(10) UNSIGNED NOT NULL CHECK (`ordering` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reporting_proposal_criterion`
--

INSERT INTO `reporting_proposal_criterion` (`id`, `name`, `description`, `type`, `required`, `active`, `ordering`) VALUES
(1, 'Financial transparency & Reporting', 'Upload file for financial transparency and reporting.', 'file', 1, 1, 1),
(2, 'Performance Monitoring & Evaluation', 'Upload file for performance monitoring and evaluation.', 'file', 1, 1, 2),
(3, 'Legal registration', 'Official legal registration document.', 'file', 1, 1, 3),
(4, 'Insurance', 'Proof of insurance.', 'file', 0, 1, 4);

-- --------------------------------------------------------

--
-- Table structure for table `reporting_proposal_criterion_response`
--

CREATE TABLE `reporting_proposal_criterion_response` (
  `id` bigint(20) NOT NULL,
  `value_text` longtext DEFAULT NULL,
  `value_file` varchar(100) DEFAULT NULL,
  `value_bool` tinyint(1) DEFAULT NULL,
  `submitted_at` datetime(6) NOT NULL,
  `criterion_id` bigint(20) NOT NULL,
  `proposal_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reporting_proposal_criterion_response`
--

INSERT INTO `reporting_proposal_criterion_response` (`id`, `value_text`, `value_file`, `value_bool`, `submitted_at`, `criterion_id`, `proposal_id`) VALUES
(1, NULL, 'proposal_criteria/school_report.pdf', NULL, '2025-07-16 08:39:57.523464', 1, 18),
(2, NULL, 'proposal_criteria/school_report_kItGYYo.pdf', NULL, '2025-07-16 08:39:57.527475', 2, 18),
(3, NULL, 'proposal_criteria/school_report_jKZUaP6.pdf', NULL, '2025-07-16 08:39:57.532486', 3, 18),
(4, NULL, 'proposal_criteria/school_report_KJgE2fv.pdf', NULL, '2025-07-16 08:39:57.536609', 4, 18);

-- --------------------------------------------------------

--
-- Table structure for table `reporting_reb_grant_budget`
--

CREATE TABLE `reporting_reb_grant_budget` (
  `id` bigint(20) NOT NULL,
  `year` varchar(10) NOT NULL,
  `total_amount` decimal(15,2) NOT NULL,
  `notes` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reporting_reb_grant_budget`
--

INSERT INTO `reporting_reb_grant_budget` (`id`, `year`, `total_amount`, `notes`, `created_at`, `updated_at`) VALUES
(1, '2025', 100000000.00, 'this s the budget for this year', '2025-07-16 07:20:40.016508', '2025-07-16 07:20:40.016508');

-- --------------------------------------------------------

--
-- Table structure for table `reporting_report`
--

CREATE TABLE `reporting_report` (
  `id` bigint(20) NOT NULL,
  `report_id` char(32) NOT NULL,
  `report_name` varchar(200) NOT NULL,
  `report_type` varchar(20) NOT NULL,
  `format` varchar(10) NOT NULL,
  `description` longtext DEFAULT NULL,
  `parameters` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`parameters`)),
  `is_scheduled` tinyint(1) NOT NULL,
  `schedule_frequency` varchar(20) DEFAULT NULL,
  `next_run_date` datetime(6) DEFAULT NULL,
  `report_file` varchar(100) DEFAULT NULL,
  `file_size` int(10) UNSIGNED NOT NULL CHECK (`file_size` >= 0),
  `status` varchar(20) NOT NULL,
  `generation_time_seconds` int(10) UNSIGNED NOT NULL CHECK (`generation_time_seconds` >= 0),
  `row_count` int(10) UNSIGNED NOT NULL CHECK (`row_count` >= 0),
  `error_message` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `generated_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint(20) NOT NULL,
  `school_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reporting_report`
--

INSERT INTO `reporting_report` (`id`, `report_id`, `report_name`, `report_type`, `format`, `description`, `parameters`, `is_scheduled`, `schedule_frequency`, `next_run_date`, `report_file`, `file_size`, `status`, `generation_time_seconds`, `row_count`, `error_message`, `created_at`, `generated_at`, `created_by_id`, `school_id`) VALUES
(1, '67584530fb1b439e84def7670c1c01cc', 'Grant Summary 1', 'grant_summary', 'pdf', 'Dummy grant_summary report', '{}', 0, NULL, NULL, '', 0, 'completed', 2, 18, NULL, '2025-07-01 08:32:00.495118', NULL, 10, 3),
(2, '2b8e3765037245a2b7f31d86b9d5eb9a', 'Grant Summary 2', 'grant_summary', 'pdf', 'Dummy grant_summary report', '{}', 0, NULL, NULL, '', 0, 'completed', 8, 13, NULL, '2025-07-01 08:32:00.497119', NULL, 10, 3),
(3, '7f80fcb52add4963b8977e6ced51684a', 'Grant Summary 3', 'grant_summary', 'pdf', 'Dummy grant_summary report', '{}', 0, NULL, NULL, '', 0, 'completed', 5, 58, NULL, '2025-07-01 08:32:00.499227', NULL, 10, 3),
(4, 'c544561b3fc34981992db458a18f9bc3', 'Budget Analysis 1', 'budget_analysis', 'pdf', 'Dummy budget_analysis report', '{}', 0, NULL, NULL, '', 0, 'completed', 7, 77, NULL, '2025-07-01 08:32:00.501592', NULL, 10, 3),
(5, 'f71138b0042b48e4b42ed3d8ed89d3ce', 'Budget Analysis 2', 'budget_analysis', 'pdf', 'Dummy budget_analysis report', '{}', 0, NULL, NULL, '', 0, 'completed', 7, 69, NULL, '2025-07-01 08:32:00.504614', NULL, 10, 3),
(6, '0b2bd49f33824b2f8762368a5039ea1d', 'Budget Analysis 3', 'budget_analysis', 'pdf', 'Dummy budget_analysis report', '{}', 0, NULL, NULL, '', 0, 'completed', 6, 38, NULL, '2025-07-01 08:32:00.507613', NULL, 10, 3),
(7, '0fbd4c92f684435e98a0a49a5890d8a7', 'School Performance 1', 'school_performance', 'pdf', 'Dummy school_performance report', '{}', 0, NULL, NULL, '', 0, 'completed', 10, 89, NULL, '2025-07-01 08:32:00.509714', NULL, 10, 3),
(8, '83e3e557ee7f4dba945ed64172f23e73', 'School Performance 2', 'school_performance', 'pdf', 'Dummy school_performance report', '{}', 0, NULL, NULL, '', 0, 'completed', 9, 84, NULL, '2025-07-01 08:32:00.511715', NULL, 10, 3),
(9, '8aebb2822e294af3ba4cdb6817836d0f', 'School Performance 3', 'school_performance', 'pdf', 'Dummy school_performance report', '{}', 0, NULL, NULL, '', 0, 'completed', 3, 90, NULL, '2025-07-01 08:32:00.513714', NULL, 10, 3),
(10, '45a27568db814105b0952c5ace106d16', 'Compliance Report 1', 'compliance_report', 'pdf', 'Dummy compliance_report report', '{}', 0, NULL, NULL, '', 0, 'completed', 3, 37, NULL, '2025-07-01 08:32:00.515715', NULL, 10, 3),
(11, '102bccb6752e40509c11b9cfdb56ae82', 'Compliance Report 2', 'compliance_report', 'pdf', 'Dummy compliance_report report', '{}', 0, NULL, NULL, '', 0, 'completed', 5, 13, NULL, '2025-07-01 08:32:00.517714', NULL, 10, 3),
(12, '63d0b41062ff41fd86d82601e1ac520c', 'Compliance Report 3', 'compliance_report', 'pdf', 'Dummy compliance_report report', '{}', 0, NULL, NULL, '', 0, 'completed', 5, 83, NULL, '2025-07-01 08:32:00.521061', NULL, 10, 3),
(13, '8df70576aa6340b49e2414cf5c92d0e1', 'Training Report 1', 'training_report', 'pdf', 'Dummy training_report report', '{}', 0, NULL, NULL, '', 0, 'completed', 4, 94, NULL, '2025-07-01 08:32:00.523761', NULL, 10, 3),
(14, '35599cc605e34b8aaf3a087984f686d5', 'Training Report 2', 'training_report', 'pdf', 'Dummy training_report report', '{}', 0, NULL, NULL, '', 0, 'completed', 7, 20, NULL, '2025-07-01 08:32:00.525766', NULL, 10, 3),
(15, '2a2626e586c94e669857bb64fe8eb8df', 'Training Report 3', 'training_report', 'pdf', 'Dummy training_report report', '{}', 0, NULL, NULL, '', 0, 'completed', 7, 58, NULL, '2025-07-01 08:32:00.527767', NULL, 10, 3),
(16, '5bbe2afde8574da5a9d1890e6c0f2ddb', 'User Activity 1', 'user_activity', 'pdf', 'Dummy user_activity report', '{}', 0, NULL, NULL, '', 0, 'completed', 9, 36, NULL, '2025-07-01 08:32:00.529928', NULL, 10, 3),
(17, '3103ee82d2f449dd9a7a345ec1c29741', 'User Activity 2', 'user_activity', 'pdf', 'Dummy user_activity report', '{}', 0, NULL, NULL, '', 0, 'completed', 7, 25, NULL, '2025-07-01 08:32:00.532929', NULL, 10, 3),
(18, 'dd666a5ac98d4222b5d42ed9833e52ad', 'User Activity 3', 'user_activity', 'pdf', 'Dummy user_activity report', '{}', 0, NULL, NULL, '', 0, 'completed', 7, 55, NULL, '2025-07-01 08:32:00.534930', NULL, 10, 3),
(19, '6524ea7b20de4461becfe59b6cbf6bdb', 'Financial Report 1', 'financial_report', 'pdf', 'Dummy financial_report report', '{}', 0, NULL, NULL, '', 0, 'completed', 6, 75, NULL, '2025-07-01 08:32:00.537935', NULL, 10, 3),
(20, '873c33572641488dac040dc8070ed1f0', 'Financial Report 2', 'financial_report', 'pdf', 'Dummy financial_report report', '{}', 0, NULL, NULL, '', 0, 'completed', 7, 73, NULL, '2025-07-01 08:32:00.541088', NULL, 10, 3),
(21, '47c6bd1ef22f4662b4b7a2616a488f5f', 'Financial Report 3', 'financial_report', 'pdf', 'Dummy financial_report report', '{}', 0, NULL, NULL, '', 0, 'completed', 5, 19, NULL, '2025-07-01 08:32:00.543657', NULL, 10, 3),
(22, '35f0e1036f1647be8c5565512c3137cb', 'Custom 1', 'custom', 'pdf', 'Dummy custom report', '{}', 0, NULL, NULL, '', 0, 'completed', 6, 55, NULL, '2025-07-01 08:32:00.545392', NULL, 10, 3),
(23, 'd7e868ec01fb46d3a5b426055dbd773c', 'Custom 2', 'custom', 'pdf', 'Dummy custom report', '{}', 0, NULL, NULL, '', 0, 'completed', 5, 83, NULL, '2025-07-01 08:32:00.547366', NULL, 10, 3),
(24, 'cf58b4bf17c34c948496821bbf588d0d', 'Custom 3', 'custom', 'pdf', 'Dummy custom report', '{}', 0, NULL, NULL, '', 0, 'completed', 8, 29, NULL, '2025-07-01 08:32:00.549506', NULL, 10, 3);

-- --------------------------------------------------------

--
-- Table structure for table `reporting_report_schedule`
--

CREATE TABLE `reporting_report_schedule` (
  `id` bigint(20) NOT NULL,
  `schedule_id` char(32) NOT NULL,
  `schedule_name` varchar(200) NOT NULL,
  `frequency` varchar(20) NOT NULL,
  `frequency_config` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`frequency_config`)),
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `next_run` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `send_email` tinyint(1) NOT NULL,
  `email_recipients` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`email_recipients`)),
  `last_run` datetime(6) DEFAULT NULL,
  `total_runs` int(10) UNSIGNED NOT NULL CHECK (`total_runs` >= 0),
  `successful_runs` int(10) UNSIGNED NOT NULL CHECK (`successful_runs` >= 0),
  `failed_runs` int(10) UNSIGNED NOT NULL CHECK (`failed_runs` >= 0),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) NOT NULL,
  `report_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reporting_supplier_criterion`
--

CREATE TABLE `reporting_supplier_criterion` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `type` varchar(10) NOT NULL,
  `required` tinyint(1) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `ordering` int(10) UNSIGNED NOT NULL CHECK (`ordering` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reporting_supplier_criterion`
--

INSERT INTO `reporting_supplier_criterion` (`id`, `name`, `description`, `type`, `required`, `active`, `ordering`) VALUES
(1, 'Legal Registration (TIN)', 'TIN certificate for legal registration.', 'file', 1, 1, 1),
(2, 'Quality assurance', 'Quality assurance documentation.', 'file', 1, 1, 2),
(3, 'RPPA certificate', 'Upload RPPA certificate.', 'file', 1, 1, 3),
(4, 'Contract proposal', 'Upload contract proposal.', 'file', 1, 1, 4),
(5, 'Payment terms', 'Specify payment terms.', 'text', 1, 1, 5);

-- --------------------------------------------------------

--
-- Table structure for table `reporting_supplier_criterion_response`
--

CREATE TABLE `reporting_supplier_criterion_response` (
  `id` bigint(20) NOT NULL,
  `value_text` longtext DEFAULT NULL,
  `value_file` varchar(100) DEFAULT NULL,
  `value_bool` tinyint(1) DEFAULT NULL,
  `submitted_at` datetime(6) NOT NULL,
  `criterion_id` bigint(20) NOT NULL,
  `supplier_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reporting_supplier_criterion_response`
--

INSERT INTO `reporting_supplier_criterion_response` (`id`, `value_text`, `value_file`, `value_bool`, `submitted_at`, `criterion_id`, `supplier_id`) VALUES
(1, NULL, 'supplier_criteria/performance_report.pdf', NULL, '2025-07-16 08:58:30.120294', 1, 18),
(2, NULL, 'supplier_criteria/performance_report_p7XLppe.pdf', NULL, '2025-07-16 08:58:30.124363', 2, 18),
(3, NULL, 'supplier_criteria/performance_report_3n2fcCC.pdf', NULL, '2025-07-16 08:58:30.128364', 3, 18),
(4, NULL, 'supplier_criteria/performance_report_hNNOV5x.pdf', NULL, '2025-07-16 08:58:30.133368', 4, 18),
(5, '300000', '', NULL, '2025-07-16 08:58:30.136003', 5, 18);

-- --------------------------------------------------------

--
-- Table structure for table `training_assessment_result`
--

CREATE TABLE `training_assessment_result` (
  `id` bigint(20) NOT NULL,
  `result_id` char(32) NOT NULL,
  `status` varchar(20) NOT NULL,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) DEFAULT NULL,
  `score` decimal(5,2) NOT NULL,
  `total_questions` int(10) UNSIGNED NOT NULL CHECK (`total_questions` >= 0),
  `correct_answers` int(10) UNSIGNED NOT NULL CHECK (`correct_answers` >= 0),
  `responses` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`responses`)),
  `time_spent_minutes` int(10) UNSIGNED NOT NULL CHECK (`time_spent_minutes` >= 0),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `assessment_id` bigint(20) NOT NULL,
  `enrollment_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `training_course_module`
--

CREATE TABLE `training_course_module` (
  `id` bigint(20) NOT NULL,
  `module_id` char(32) NOT NULL,
  `module_title` varchar(200) NOT NULL,
  `module_type` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `content` longtext DEFAULT NULL,
  `duration_minutes` int(10) UNSIGNED NOT NULL CHECK (`duration_minutes` >= 0),
  `order` int(10) UNSIGNED NOT NULL CHECK (`order` >= 0),
  `is_required` tinyint(1) NOT NULL,
  `passing_score` int(10) UNSIGNED NOT NULL CHECK (`passing_score` >= 0),
  `module_file` varchar(100) DEFAULT NULL,
  `supplementary_files` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`supplementary_files`)),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `course_id` bigint(20) NOT NULL,
  `created_by_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `training_module_progress`
--

CREATE TABLE `training_module_progress` (
  `id` bigint(20) NOT NULL,
  `progress_id` char(32) NOT NULL,
  `status` varchar(20) NOT NULL,
  `start_date` datetime(6) DEFAULT NULL,
  `completion_date` datetime(6) DEFAULT NULL,
  `score` decimal(5,2) NOT NULL,
  `attempts` int(10) UNSIGNED NOT NULL CHECK (`attempts` >= 0),
  `time_spent_minutes` int(10) UNSIGNED NOT NULL CHECK (`time_spent_minutes` >= 0),
  `notes` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `enrollment_id` bigint(20) NOT NULL,
  `module_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `training_training_assessment`
--

CREATE TABLE `training_training_assessment` (
  `id` bigint(20) NOT NULL,
  `assessment_id` char(32) NOT NULL,
  `assessment_title` varchar(200) NOT NULL,
  `assessment_type` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `instructions` longtext DEFAULT NULL,
  `time_limit_minutes` int(10) UNSIGNED NOT NULL CHECK (`time_limit_minutes` >= 0),
  `passing_score` int(10) UNSIGNED NOT NULL CHECK (`passing_score` >= 0),
  `max_attempts` int(10) UNSIGNED NOT NULL CHECK (`max_attempts` >= 0),
  `is_required` tinyint(1) NOT NULL,
  `questions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`questions`)),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) NOT NULL,
  `module_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `training_training_category`
--

CREATE TABLE `training_training_category` (
  `id` bigint(20) NOT NULL,
  `category_id` char(32) NOT NULL,
  `category_name` varchar(100) NOT NULL,
  `category_type` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `requires_approval` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `training_training_category`
--

INSERT INTO `training_training_category` (`id`, `category_id`, `category_name`, `category_type`, `description`, `is_active`, `requires_approval`, `created_at`, `updated_at`, `created_by_id`) VALUES
(1, '8f0e4a4248474377b3457c2a94b4e69d', 'Demo Category', 'grant_management', 'Demo', 1, 0, '2025-06-30 18:57:52.611697', '2025-06-30 18:57:52.611697', 9);

-- --------------------------------------------------------

--
-- Table structure for table `training_training_certificate`
--

CREATE TABLE `training_training_certificate` (
  `id` bigint(20) NOT NULL,
  `certificate_id` char(32) NOT NULL,
  `certificate_type` varchar(20) NOT NULL,
  `certificate_title` varchar(200) NOT NULL,
  `certificate_number` varchar(50) NOT NULL,
  `issue_date` datetime(6) NOT NULL,
  `expiry_date` datetime(6) DEFAULT NULL,
  `description` longtext NOT NULL,
  `achievements` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`achievements`)),
  `certificate_file` varchar(100) DEFAULT NULL,
  `is_valid` tinyint(1) NOT NULL,
  `is_revoked` tinyint(1) NOT NULL,
  `revocation_reason` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL,
  `enrollment_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `training_training_course`
--

CREATE TABLE `training_training_course` (
  `id` bigint(20) NOT NULL,
  `course_id` char(32) NOT NULL,
  `course_title` varchar(200) NOT NULL,
  `course_code` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `learning_objectives` longtext NOT NULL,
  `target_audience` longtext NOT NULL,
  `course_level` varchar(20) NOT NULL,
  `course_format` varchar(20) NOT NULL,
  `duration_hours` int(10) UNSIGNED NOT NULL CHECK (`duration_hours` >= 0),
  `max_participants` int(10) UNSIGNED NOT NULL CHECK (`max_participants` >= 0),
  `course_materials` longtext DEFAULT NULL,
  `prerequisites` longtext DEFAULT NULL,
  `certification_requirements` longtext DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `approval_date` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_by_id` bigint(20) DEFAULT NULL,
  `category_id` bigint(20) NOT NULL,
  `created_by_id` bigint(20) NOT NULL,
  `guide_document` varchar(100) DEFAULT NULL,
  `video_url` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `training_training_course`
--

INSERT INTO `training_training_course` (`id`, `course_id`, `course_title`, `course_code`, `description`, `learning_objectives`, `target_audience`, `course_level`, `course_format`, `duration_hours`, `max_participants`, `course_materials`, `prerequisites`, `certification_requirements`, `is_active`, `is_approved`, `approval_date`, `created_at`, `updated_at`, `approved_by_id`, `category_id`, `created_by_id`, `guide_document`, `video_url`) VALUES
(2, 'c5b1454e84d5472f81a641563531d508', 'Demo Course', 'DEMO1', 'Demo', 'Learn', 'All', 'beginner', 'online', 10, 30, NULL, NULL, NULL, 1, 1, NULL, '2025-06-30 18:57:52.615134', '2025-06-30 18:57:52.615134', NULL, 1, 9, NULL, NULL),
(3, '3023358ab24e4a7ea3c9274569a40124', 'use grant well', 'TC2025070003', 'This is the course to give you skills for how to use the grants well', 'Skills', 'admins,auditors, school administration,teachers', 'beginner', 'online', 2, 100, 'list of key strategies', 'finance management', 'none', 1, 0, NULL, '2025-07-15 18:44:53.611729', '2025-07-15 18:44:53.611729', NULL, 1, 6, '', 'https://www.youtube.com/watch?v=07rzH-EQKzk');

-- --------------------------------------------------------

--
-- Table structure for table `training_training_enrollment`
--

CREATE TABLE `training_training_enrollment` (
  `id` bigint(20) NOT NULL,
  `enrollment_id` char(32) NOT NULL,
  `enrollment_date` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `start_date` datetime(6) DEFAULT NULL,
  `completion_date` datetime(6) DEFAULT NULL,
  `progress_percentage` decimal(5,2) NOT NULL,
  `final_score` decimal(5,2) NOT NULL,
  `is_certified` tinyint(1) NOT NULL,
  `certification_date` datetime(6) DEFAULT NULL,
  `enrollment_notes` longtext DEFAULT NULL,
  `completion_notes` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `course_id` bigint(20) NOT NULL,
  `session_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `training_training_enrollment`
--

INSERT INTO `training_training_enrollment` (`id`, `enrollment_id`, `enrollment_date`, `status`, `start_date`, `completion_date`, `progress_percentage`, `final_score`, `is_certified`, `certification_date`, `enrollment_notes`, `completion_notes`, `created_at`, `updated_at`, `course_id`, `session_id`, `user_id`) VALUES
(1, '3eb93a912a7141c6aaf147b1b86ae93f', '2025-06-30 19:00:57.657882', 'enrolled', NULL, NULL, 0.00, 0.00, 0, NULL, NULL, NULL, '2025-06-30 19:00:57.658164', '2025-06-30 19:00:57.658164', 2, 1, 6),
(6, 'e2f99765d72b42a3b366e99ea46b34c3', '2025-07-14 13:02:13.931259', 'enrolled', NULL, NULL, 0.00, 0.00, 0, NULL, NULL, NULL, '2025-07-14 13:02:13.931259', '2025-07-14 13:02:13.931259', 2, 1, 16);

-- --------------------------------------------------------

--
-- Table structure for table `training_training_session`
--

CREATE TABLE `training_training_session` (
  `id` bigint(20) NOT NULL,
  `session_id` char(32) NOT NULL,
  `session_title` varchar(200) NOT NULL,
  `description` longtext DEFAULT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `location` varchar(200) DEFAULT NULL,
  `max_participants` int(10) UNSIGNED NOT NULL CHECK (`max_participants` >= 0),
  `current_participants` int(10) UNSIGNED NOT NULL CHECK (`current_participants` >= 0),
  `status` varchar(20) NOT NULL,
  `session_notes` longtext DEFAULT NULL,
  `completion_notes` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `course_id` bigint(20) NOT NULL,
  `created_by_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `training_training_session`
--

INSERT INTO `training_training_session` (`id`, `session_id`, `session_title`, `description`, `start_date`, `end_date`, `location`, `max_participants`, `current_participants`, `status`, `session_notes`, `completion_notes`, `created_at`, `updated_at`, `course_id`, `created_by_id`) VALUES
(1, '21ce62a8a4c8441283801c3a50b88ec6', 'Demo Session', NULL, '2025-06-30 18:57:52.617124', '2025-06-30 18:57:52.617124', NULL, 0, 0, 'scheduled', NULL, NULL, '2025-06-30 18:57:52.621151', '2025-06-30 18:57:52.621151', 2, 9);

-- --------------------------------------------------------

--
-- Table structure for table `training_training_session_facilitators`
--

CREATE TABLE `training_training_session_facilitators` (
  `id` bigint(20) NOT NULL,
  `trainingsession_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ai_engine_aimodelstatus`
--
ALTER TABLE `ai_engine_aimodelstatus`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `component` (`component`);

--
-- Indexes for table `ai_engine_ai_performance_metrics`
--
ALTER TABLE `ai_engine_ai_performance_metrics`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `metric_id` (`metric_id`);

--
-- Indexes for table `ai_engine_allocation_algorithm`
--
ALTER TABLE `ai_engine_allocation_algorithm`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `algorithm_id` (`algorithm_id`),
  ADD UNIQUE KEY `algorithm_name` (`algorithm_name`),
  ADD KEY `ai_engine_allocation_created_by_id_6e8d067f_fk_core_user` (`created_by_id`);

--
-- Indexes for table `ai_engine_allocation_factor`
--
ALTER TABLE `ai_engine_allocation_factor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `factor_id` (`factor_id`),
  ADD UNIQUE KEY `factor_name` (`factor_name`),
  ADD KEY `ai_engine_allocation_created_by_id_770dc5bd_fk_core_user` (`created_by_id`);

--
-- Indexes for table `ai_engine_allocation_run`
--
ALTER TABLE `ai_engine_allocation_run`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `run_id` (`run_id`),
  ADD KEY `ai_engine_allocation_algorithm_id_d442ae39_fk_ai_engine` (`algorithm_id`),
  ADD KEY `ai_engine_allocation_run_created_by_id_58e155bf_fk_core_user_id` (`created_by_id`);

--
-- Indexes for table `ai_engine_optimization_recommendation`
--
ALTER TABLE `ai_engine_optimization_recommendation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `recommendation_id` (`recommendation_id`),
  ADD KEY `ai_engine_optimizati_created_by_id_6f67c7cc_fk_core_user` (`created_by_id`),
  ADD KEY `ai_engine_optimizati_implemented_by_id_090113e3_fk_core_user` (`implemented_by_id`),
  ADD KEY `ai_engine_optimizati_proposal_id_7f74558d_fk_grants_gr` (`proposal_id`),
  ADD KEY `ai_engine_optimizati_school_id_0c03dc63_fk_core_scho` (`school_id`);

--
-- Indexes for table `ai_engine_proposalanomaly`
--
ALTER TABLE `ai_engine_proposalanomaly`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ai_engine_proposalan_proposal_id_5b085c8d_fk_grants_gr` (`proposal_id`);

--
-- Indexes for table `ai_engine_proposalprediction`
--
ALTER TABLE `ai_engine_proposalprediction`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `proposal_id` (`proposal_id`);

--
-- Indexes for table `ai_engine_proposal_allocation_score`
--
ALTER TABLE `ai_engine_proposal_allocation_score`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `score_id` (`score_id`),
  ADD UNIQUE KEY `ai_engine_proposal_alloc_allocation_run_id_propos_e94ec3e1_uniq` (`allocation_run_id`,`proposal_id`),
  ADD KEY `ai_engine_proposal_a_proposal_id_ca34296d_fk_grants_gr` (`proposal_id`);

--
-- Indexes for table `ai_engine_recommendationaction`
--
ALTER TABLE `ai_engine_recommendationaction`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ai_engine_recommendation_user_id_proposal_title_94f7b688_uniq` (`user_id`,`proposal_title`);

--
-- Indexes for table `ai_engine_risk_assessment`
--
ALTER TABLE `ai_engine_risk_assessment`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `risk_id` (`risk_id`),
  ADD KEY `ai_engine_risk_assessment_created_by_id_35bcb65d_fk_core_user_id` (`created_by_id`),
  ADD KEY `ai_engine_risk_asses_proposal_id_c8c151f2_fk_grants_gr` (`proposal_id`),
  ADD KEY `ai_engine_risk_asses_resolved_by_id_29166d7f_fk_core_user` (`resolved_by_id`),
  ADD KEY `ai_engine_risk_assessment_school_id_bcb72f81_fk_core_school_id` (`school_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `budget_budget_category`
--
ALTER TABLE `budget_budget_category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `category_id` (`category_id`);

--
-- Indexes for table `budget_budget_line_item`
--
ALTER TABLE `budget_budget_line_item`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `line_item_id` (`line_item_id`),
  ADD KEY `budget_budget_line_i_budget_category_id_ad34c87c_fk_budget_bu` (`budget_category_id`),
  ADD KEY `budget_budget_line_item_created_by_id_219277f8_fk_core_user_id` (`created_by_id`),
  ADD KEY `budget_budget_line_i_related_proposal_id_ca9f7066_fk_grants_gr` (`related_proposal_id`),
  ADD KEY `budget_budget_line_i_school_budget_id_308b2f14_fk_budget_sc` (`school_budget_id`);

--
-- Indexes for table `budget_budget_period`
--
ALTER TABLE `budget_budget_period`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `period_id` (`period_id`),
  ADD UNIQUE KEY `period_name` (`period_name`),
  ADD KEY `budget_budget_period_created_by_id_f033cea1_fk_core_user_id` (`created_by_id`);

--
-- Indexes for table `budget_budget_report`
--
ALTER TABLE `budget_budget_report`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `report_id` (`report_id`),
  ADD KEY `budget_budget_report_generated_by_id_c40c9e4d_fk_core_user_id` (`generated_by_id`),
  ADD KEY `budget_budget_report_school_budget_id_414a0405_fk_budget_sc` (`school_budget_id`);

--
-- Indexes for table `budget_budget_transfer`
--
ALTER TABLE `budget_budget_transfer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `transfer_id` (`transfer_id`),
  ADD KEY `budget_budget_transfer_approved_by_id_fbf3e0a0_fk_core_user_id` (`approved_by_id`),
  ADD KEY `budget_budget_transfer_created_by_id_fae478e9_fk_core_user_id` (`created_by_id`),
  ADD KEY `budget_budget_transf_destination_line_ite_f471d759_fk_budget_bu` (`destination_line_item_id`),
  ADD KEY `budget_budget_transf_source_line_item_id_b13da18c_fk_budget_bu` (`source_line_item_id`);

--
-- Indexes for table `budget_expenditure`
--
ALTER TABLE `budget_expenditure`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `expenditure_id` (`expenditure_id`),
  ADD KEY `budget_expenditure_approved_by_id_3f0bb80f_fk_core_user_id` (`approved_by_id`),
  ADD KEY `budget_expenditure_budget_line_item_id_9507dab3_fk_budget_bu` (`budget_line_item_id`),
  ADD KEY `budget_expenditure_created_by_id_09348f00_fk_core_user_id` (`created_by_id`);

--
-- Indexes for table `budget_school_budget`
--
ALTER TABLE `budget_school_budget`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `budget_id` (`budget_id`),
  ADD KEY `budget_school_budget_approved_by_id_70465744_fk_core_user_id` (`approved_by_id`),
  ADD KEY `budget_school_budget_budget_period_id_d9dd972c_fk_budget_bu` (`budget_period_id`),
  ADD KEY `budget_school_budget_created_by_id_debe0a95_fk_core_user_id` (`created_by_id`),
  ADD KEY `budget_school_budget_school_id_b14fecbe_fk_core_school_id` (`school_id`);

--
-- Indexes for table `community_announcement`
--
ALTER TABLE `community_announcement`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `announcement_id` (`announcement_id`),
  ADD KEY `community_announcement_created_by_id_1908c9a7_fk_core_user_id` (`created_by_id`);

--
-- Indexes for table `community_announcement_target_schools`
--
ALTER TABLE `community_announcement_target_schools`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `community_announcement_t_announcement_id_school_i_d3f79303_uniq` (`announcement_id`,`school_id`),
  ADD KEY `community_announceme_school_id_206b4bae_fk_core_scho` (`school_id`);

--
-- Indexes for table `community_community_event`
--
ALTER TABLE `community_community_event`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `event_id` (`event_id`),
  ADD KEY `community_community__contact_person_id_ce0f9cae_fk_core_user` (`contact_person_id`),
  ADD KEY `community_community_event_created_by_id_b20a807c_fk_core_user_id` (`created_by_id`);

--
-- Indexes for table `community_community_event_organizers`
--
ALTER TABLE `community_community_event_organizers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `community_community_even_communityevent_id_user_i_29adfc0b_uniq` (`communityevent_id`,`user_id`),
  ADD KEY `community_community__user_id_07019dfd_fk_core_user` (`user_id`);

--
-- Indexes for table `community_community_event_target_schools`
--
ALTER TABLE `community_community_event_target_schools`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `community_community_even_communityevent_id_school_54f79ac7_uniq` (`communityevent_id`,`school_id`),
  ADD KEY `community_community__school_id_c488aa0e_fk_core_scho` (`school_id`);

--
-- Indexes for table `community_community_forum`
--
ALTER TABLE `community_community_forum`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `forum_id` (`forum_id`),
  ADD UNIQUE KEY `forum_name` (`forum_name`),
  ADD KEY `community_community_forum_created_by_id_a7f09439_fk_core_user_id` (`created_by_id`),
  ADD KEY `community_community_forum_school_id_3ccf3391_fk_core_school_id` (`school_id`);

--
-- Indexes for table `community_community_forum_moderators`
--
ALTER TABLE `community_community_forum_moderators`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `community_community_foru_communityforum_id_user_i_027517ea_uniq` (`communityforum_id`,`user_id`),
  ADD KEY `community_community__user_id_1ed27362_fk_core_user` (`user_id`);

--
-- Indexes for table `community_community_message`
--
ALTER TABLE `community_community_message`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `message_id` (`message_id`),
  ADD KEY `community_community__replied_to_id_6c587ec2_fk_community` (`replied_to_id`),
  ADD KEY `community_community_message_school_id_31ff80d5_fk_core_school_id` (`school_id`),
  ADD KEY `community_community_message_sender_id_96c39389_fk_core_user_id` (`sender_id`);

--
-- Indexes for table `community_community_message_recipients`
--
ALTER TABLE `community_community_message_recipients`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `community_community_mess_communitymessage_id_user_8ced3f2e_uniq` (`communitymessage_id`,`user_id`),
  ADD KEY `community_community__user_id_973a2b4a_fk_core_user` (`user_id`);

--
-- Indexes for table `community_feedback`
--
ALTER TABLE `community_feedback`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `feedback_id` (`feedback_id`),
  ADD KEY `community_feedback_resolved_by_id_974f2645_fk_core_user_id` (`resolved_by_id`),
  ADD KEY `community_feedback_reviewed_by_id_292508a6_fk_core_user_id` (`reviewed_by_id`),
  ADD KEY `community_feedback_school_id_c7d56c49_fk_core_school_id` (`school_id`),
  ADD KEY `community_feedback_submitted_by_id_4fa007ce_fk_core_user_id` (`submitted_by_id`);

--
-- Indexes for table `community_forum_post`
--
ALTER TABLE `community_forum_post`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `post_id` (`post_id`),
  ADD KEY `community_forum_post_created_by_id_b7767713_fk_core_user_id` (`created_by_id`),
  ADD KEY `community_forum_post_edited_by_id_a5206ed4_fk_core_user_id` (`edited_by_id`),
  ADD KEY `community_forum_post_parent_post_id_a0b6f13d_fk_community` (`parent_post_id`),
  ADD KEY `community_forum_post_topic_id_dbaba187_fk_community` (`topic_id`);

--
-- Indexes for table `community_forum_topic`
--
ALTER TABLE `community_forum_topic`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `topic_id` (`topic_id`),
  ADD KEY `community_forum_topic_created_by_id_3a5c9011_fk_core_user_id` (`created_by_id`),
  ADD KEY `community_forum_topi_forum_id_9e4d0d58_fk_community` (`forum_id`),
  ADD KEY `community_forum_topic_last_post_by_id_148f12d1_fk_core_user_id` (`last_post_by_id`);

--
-- Indexes for table `core_auditlog`
--
ALTER TABLE `core_auditlog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_auditlog_user_id_3797aaab_fk_core_user_id` (`user_id`);

--
-- Indexes for table `core_district`
--
ALTER TABLE `core_district`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `district_id` (`district_id`),
  ADD UNIQUE KEY `district_name` (`district_name`),
  ADD UNIQUE KEY `district_code` (`district_code`);

--
-- Indexes for table `core_school`
--
ALTER TABLE `core_school`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `school_id` (`school_id`),
  ADD UNIQUE KEY `school_name` (`school_name`),
  ADD UNIQUE KEY `school_code` (`school_code`),
  ADD KEY `core_school_created_by_id_0559e6ce_fk_core_user_id` (`created_by_id`);

--
-- Indexes for table `core_school_user`
--
ALTER TABLE `core_school_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `core_school_user_user_id_school_id_f5b07b76_uniq` (`user_id`,`school_id`),
  ADD KEY `core_school_user_assigned_by_id_a9eb8cb8_fk_core_user_id` (`assigned_by_id`),
  ADD KEY `core_school_user_school_id_df605e87_fk_core_school_id` (`school_id`);

--
-- Indexes for table `core_system_configuration`
--
ALTER TABLE `core_system_configuration`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `config_key` (`config_key`),
  ADD KEY `core_system_configuration_created_by_id_102929e6_fk_core_user_id` (`created_by_id`);

--
-- Indexes for table `core_user`
--
ALTER TABLE `core_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `core_user_groups`
--
ALTER TABLE `core_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `core_user_groups_user_id_group_id_c82fcad1_uniq` (`user_id`,`group_id`),
  ADD KEY `core_user_groups_group_id_fe8c697f_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `core_user_user_permissions`
--
ALTER TABLE `core_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `core_user_user_permissions_user_id_permission_id_73ea0daa_uniq` (`user_id`,`permission_id`),
  ADD KEY `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_core_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `grants_fund_allocation`
--
ALTER TABLE `grants_fund_allocation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `allocation_id` (`allocation_id`),
  ADD KEY `grants_fund_allocation_allocated_by_id_f839097f_fk_core_user_id` (`allocated_by_id`),
  ADD KEY `grants_fund_allocation_disbursed_by_id_a8908e53_fk_core_user_id` (`disbursed_by_id`),
  ADD KEY `grants_fund_allocati_proposal_id_19011cef_fk_grants_gr` (`proposal_id`);

--
-- Indexes for table `grants_grant_category`
--
ALTER TABLE `grants_grant_category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `category_id` (`category_id`),
  ADD UNIQUE KEY `category_name` (`category_name`),
  ADD KEY `grants_grant_category_created_by_id_aacee909_fk_core_user_id` (`created_by_id`);

--
-- Indexes for table `grants_grant_proposal`
--
ALTER TABLE `grants_grant_proposal`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `proposal_id` (`proposal_id`),
  ADD UNIQUE KEY `proposal_code` (`proposal_code`),
  ADD KEY `grants_grant_proposal_approved_by_id_009dfe80_fk_core_user_id` (`approved_by_id`),
  ADD KEY `grants_grant_proposal_created_by_id_0b9769a3_fk_core_user_id` (`created_by_id`),
  ADD KEY `grants_grant_proposa_grant_category_id_4b5c7fe9_fk_grants_gr` (`grant_category_id`),
  ADD KEY `grants_grant_proposal_school_id_bb24290d_fk_core_school_id` (`school_id`);

--
-- Indexes for table `grants_proposal_budget`
--
ALTER TABLE `grants_proposal_budget`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `budget_id` (`budget_id`),
  ADD KEY `grants_proposal_budget_created_by_id_db742513_fk_core_user_id` (`created_by_id`),
  ADD KEY `grants_proposal_budg_proposal_id_06dcccf4_fk_grants_gr` (`proposal_id`);

--
-- Indexes for table `grants_proposal_document`
--
ALTER TABLE `grants_proposal_document`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `document_id` (`document_id`),
  ADD KEY `grants_proposal_docu_proposal_id_02c76dbe_fk_grants_gr` (`proposal_id`),
  ADD KEY `grants_proposal_document_uploaded_by_id_25303237_fk_core_user_id` (`uploaded_by_id`);

--
-- Indexes for table `grants_proposal_review`
--
ALTER TABLE `grants_proposal_review`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `review_id` (`review_id`),
  ADD KEY `grants_proposal_revi_proposal_id_ad8472a6_fk_grants_gr` (`proposal_id`),
  ADD KEY `grants_proposal_review_reviewer_id_50ac1cc8_fk_core_user_id` (`reviewer_id`);

--
-- Indexes for table `procurement_bid`
--
ALTER TABLE `procurement_bid`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `bid_id` (`bid_id`),
  ADD KEY `procurement_bid_supplier_id_2e696167_fk_core_user_id` (`supplier_id`),
  ADD KEY `procurement_bid_tender_id_3b6ca2a1_fk_procurement_tender_id` (`tender_id`);

--
-- Indexes for table `procurement_tender`
--
ALTER TABLE `procurement_tender`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tender_id` (`tender_id`),
  ADD KEY `procurement_tender_created_by_id_94b01d94_fk_core_user_id` (`created_by_id`),
  ADD KEY `procurement_tender_school_id_7549296b_fk_core_school_id` (`school_id`);

--
-- Indexes for table `procurement_tenderdocument`
--
ALTER TABLE `procurement_tenderdocument`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `document_id` (`document_id`),
  ADD KEY `procurement_tenderdo_tender_id_e8f4ef72_fk_procureme` (`tender_id`),
  ADD KEY `procurement_tenderdo_uploaded_by_id_5d012aab_fk_core_user` (`uploaded_by_id`);

--
-- Indexes for table `procurement_tenderstatushistory`
--
ALTER TABLE `procurement_tenderstatushistory`
  ADD PRIMARY KEY (`id`),
  ADD KEY `procurement_tenderst_changed_by_id_22862556_fk_core_user` (`changed_by_id`),
  ADD KEY `procurement_tenderst_tender_id_0a47d206_fk_procureme` (`tender_id`);

--
-- Indexes for table `reporting_analytics_event`
--
ALTER TABLE `reporting_analytics_event`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `event_id` (`event_id`),
  ADD KEY `reporting_analytics_event_user_id_c0f6380a_fk_core_user_id` (`user_id`);

--
-- Indexes for table `reporting_dashboard`
--
ALTER TABLE `reporting_dashboard`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `dashboard_id` (`dashboard_id`),
  ADD UNIQUE KEY `reporting_dashboard_user_id_dashboard_name_b99a5920_uniq` (`user_id`,`dashboard_name`),
  ADD KEY `reporting_dashboard_school_id_63c95789_fk_core_school_id` (`school_id`);

--
-- Indexes for table `reporting_dashboard_widget`
--
ALTER TABLE `reporting_dashboard_widget`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `widget_id` (`widget_id`),
  ADD KEY `reporting_dashboard__dashboard_id_c2f6d402_fk_reporting` (`dashboard_id`);

--
-- Indexes for table `reporting_data_export`
--
ALTER TABLE `reporting_data_export`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `export_id` (`export_id`),
  ADD KEY `reporting_data_export_school_id_04c5cdd9_fk_core_school_id` (`school_id`),
  ADD KEY `reporting_data_export_user_id_c4372e22_fk_core_user_id` (`user_id`);

--
-- Indexes for table `reporting_kpi`
--
ALTER TABLE `reporting_kpi`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `kpi_id` (`kpi_id`),
  ADD UNIQUE KEY `kpi_name` (`kpi_name`),
  ADD KEY `reporting_kpi_created_by_id_a9ce979b_fk_core_user_id` (`created_by_id`);

--
-- Indexes for table `reporting_kpi_value`
--
ALTER TABLE `reporting_kpi_value`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `value_id` (`value_id`),
  ADD UNIQUE KEY `reporting_kpi_value_kpi_id_school_id_measure_27ec3159_uniq` (`kpi_id`,`school_id`,`measurement_date`),
  ADD KEY `reporting_kpi_value_calculated_by_id_b25167d0_fk_core_user_id` (`calculated_by_id`),
  ADD KEY `reporting_kpi_value_school_id_10ba7d7e_fk_core_school_id` (`school_id`);

--
-- Indexes for table `reporting_proposal_criterion`
--
ALTER TABLE `reporting_proposal_criterion`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reporting_proposal_criterion_response`
--
ALTER TABLE `reporting_proposal_criterion_response`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reporting_proposal_crite_proposal_id_criterion_id_38241b2c_uniq` (`proposal_id`,`criterion_id`),
  ADD KEY `reporting_proposal_c_criterion_id_6ddfba61_fk_reporting` (`criterion_id`);

--
-- Indexes for table `reporting_reb_grant_budget`
--
ALTER TABLE `reporting_reb_grant_budget`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reporting_report`
--
ALTER TABLE `reporting_report`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `report_id` (`report_id`),
  ADD KEY `reporting_report_created_by_id_1c6d7e8d_fk_core_user_id` (`created_by_id`),
  ADD KEY `reporting_report_school_id_96fae51e_fk_core_school_id` (`school_id`);

--
-- Indexes for table `reporting_report_schedule`
--
ALTER TABLE `reporting_report_schedule`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `schedule_id` (`schedule_id`),
  ADD KEY `reporting_report_schedule_created_by_id_7fc1a5db_fk_core_user_id` (`created_by_id`),
  ADD KEY `reporting_report_sch_report_id_32be7f8f_fk_reporting` (`report_id`);

--
-- Indexes for table `reporting_supplier_criterion`
--
ALTER TABLE `reporting_supplier_criterion`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reporting_supplier_criterion_response`
--
ALTER TABLE `reporting_supplier_criterion_response`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reporting_supplier_crite_supplier_id_criterion_id_2ed3d6cf_uniq` (`supplier_id`,`criterion_id`),
  ADD KEY `reporting_supplier_c_criterion_id_a368d50d_fk_reporting` (`criterion_id`);

--
-- Indexes for table `training_assessment_result`
--
ALTER TABLE `training_assessment_result`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `result_id` (`result_id`),
  ADD KEY `training_assessment__assessment_id_1bd66fce_fk_training_` (`assessment_id`),
  ADD KEY `training_assessment__enrollment_id_ea114498_fk_training_` (`enrollment_id`);

--
-- Indexes for table `training_course_module`
--
ALTER TABLE `training_course_module`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `module_id` (`module_id`),
  ADD UNIQUE KEY `training_course_module_course_id_order_588f851f_uniq` (`course_id`,`order`),
  ADD KEY `training_course_module_created_by_id_398a5729_fk_core_user_id` (`created_by_id`);

--
-- Indexes for table `training_module_progress`
--
ALTER TABLE `training_module_progress`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `progress_id` (`progress_id`),
  ADD UNIQUE KEY `training_module_progress_enrollment_id_module_id_03f048b8_uniq` (`enrollment_id`,`module_id`),
  ADD KEY `training_module_prog_module_id_00e815d4_fk_training_` (`module_id`);

--
-- Indexes for table `training_training_assessment`
--
ALTER TABLE `training_training_assessment`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `assessment_id` (`assessment_id`),
  ADD KEY `training_training_as_created_by_id_34515157_fk_core_user` (`created_by_id`),
  ADD KEY `training_training_as_module_id_8f262f53_fk_training_` (`module_id`);

--
-- Indexes for table `training_training_category`
--
ALTER TABLE `training_training_category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `category_id` (`category_id`),
  ADD UNIQUE KEY `category_name` (`category_name`),
  ADD KEY `training_training_ca_created_by_id_c8470dc7_fk_core_user` (`created_by_id`);

--
-- Indexes for table `training_training_certificate`
--
ALTER TABLE `training_training_certificate`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `certificate_id` (`certificate_id`),
  ADD UNIQUE KEY `certificate_number` (`certificate_number`),
  ADD KEY `training_training_ce_created_by_id_5572d734_fk_core_user` (`created_by_id`),
  ADD KEY `training_training_ce_enrollment_id_8c0fd39e_fk_training_` (`enrollment_id`);

--
-- Indexes for table `training_training_course`
--
ALTER TABLE `training_training_course`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `course_id` (`course_id`),
  ADD UNIQUE KEY `course_title` (`course_title`),
  ADD UNIQUE KEY `course_code` (`course_code`),
  ADD KEY `training_training_course_approved_by_id_1c66e147_fk_core_user_id` (`approved_by_id`),
  ADD KEY `training_training_co_category_id_edd02ba2_fk_training_` (`category_id`),
  ADD KEY `training_training_course_created_by_id_df87213f_fk_core_user_id` (`created_by_id`);

--
-- Indexes for table `training_training_enrollment`
--
ALTER TABLE `training_training_enrollment`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `enrollment_id` (`enrollment_id`),
  ADD UNIQUE KEY `training_training_enroll_user_id_course_id_sessio_fd62a37a_uniq` (`user_id`,`course_id`,`session_id`),
  ADD KEY `training_training_en_course_id_3bebaa9a_fk_training_` (`course_id`),
  ADD KEY `training_training_en_session_id_cfc36558_fk_training_` (`session_id`);

--
-- Indexes for table `training_training_session`
--
ALTER TABLE `training_training_session`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `session_id` (`session_id`),
  ADD KEY `training_training_se_course_id_d253b600_fk_training_` (`course_id`),
  ADD KEY `training_training_session_created_by_id_4101952f_fk_core_user_id` (`created_by_id`);

--
-- Indexes for table `training_training_session_facilitators`
--
ALTER TABLE `training_training_session_facilitators`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `training_training_sessio_trainingsession_id_user__a8a3eba8_uniq` (`trainingsession_id`,`user_id`),
  ADD KEY `training_training_se_user_id_86bf2066_fk_core_user` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ai_engine_aimodelstatus`
--
ALTER TABLE `ai_engine_aimodelstatus`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `ai_engine_ai_performance_metrics`
--
ALTER TABLE `ai_engine_ai_performance_metrics`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ai_engine_allocation_algorithm`
--
ALTER TABLE `ai_engine_allocation_algorithm`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ai_engine_allocation_factor`
--
ALTER TABLE `ai_engine_allocation_factor`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ai_engine_allocation_run`
--
ALTER TABLE `ai_engine_allocation_run`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ai_engine_optimization_recommendation`
--
ALTER TABLE `ai_engine_optimization_recommendation`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ai_engine_proposalanomaly`
--
ALTER TABLE `ai_engine_proposalanomaly`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=133;

--
-- AUTO_INCREMENT for table `ai_engine_proposalprediction`
--
ALTER TABLE `ai_engine_proposalprediction`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `ai_engine_proposal_allocation_score`
--
ALTER TABLE `ai_engine_proposal_allocation_score`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ai_engine_recommendationaction`
--
ALTER TABLE `ai_engine_recommendationaction`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `ai_engine_risk_assessment`
--
ALTER TABLE `ai_engine_risk_assessment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=273;

--
-- AUTO_INCREMENT for table `budget_budget_category`
--
ALTER TABLE `budget_budget_category`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `budget_budget_line_item`
--
ALTER TABLE `budget_budget_line_item`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `budget_budget_period`
--
ALTER TABLE `budget_budget_period`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `budget_budget_report`
--
ALTER TABLE `budget_budget_report`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `budget_budget_transfer`
--
ALTER TABLE `budget_budget_transfer`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `budget_expenditure`
--
ALTER TABLE `budget_expenditure`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `budget_school_budget`
--
ALTER TABLE `budget_school_budget`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `community_announcement`
--
ALTER TABLE `community_announcement`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `community_announcement_target_schools`
--
ALTER TABLE `community_announcement_target_schools`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `community_community_event`
--
ALTER TABLE `community_community_event`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `community_community_event_organizers`
--
ALTER TABLE `community_community_event_organizers`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `community_community_event_target_schools`
--
ALTER TABLE `community_community_event_target_schools`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `community_community_forum`
--
ALTER TABLE `community_community_forum`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `community_community_forum_moderators`
--
ALTER TABLE `community_community_forum_moderators`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `community_community_message`
--
ALTER TABLE `community_community_message`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `community_community_message_recipients`
--
ALTER TABLE `community_community_message_recipients`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `community_feedback`
--
ALTER TABLE `community_feedback`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `community_forum_post`
--
ALTER TABLE `community_forum_post`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `community_forum_topic`
--
ALTER TABLE `community_forum_topic`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_auditlog`
--
ALTER TABLE `core_auditlog`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `core_district`
--
ALTER TABLE `core_district`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_school`
--
ALTER TABLE `core_school`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `core_school_user`
--
ALTER TABLE `core_school_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_system_configuration`
--
ALTER TABLE `core_system_configuration`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_user`
--
ALTER TABLE `core_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `core_user_groups`
--
ALTER TABLE `core_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_user_user_permissions`
--
ALTER TABLE `core_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=70;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `grants_fund_allocation`
--
ALTER TABLE `grants_fund_allocation`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `grants_grant_category`
--
ALTER TABLE `grants_grant_category`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `grants_grant_proposal`
--
ALTER TABLE `grants_grant_proposal`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `grants_proposal_budget`
--
ALTER TABLE `grants_proposal_budget`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `grants_proposal_document`
--
ALTER TABLE `grants_proposal_document`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `grants_proposal_review`
--
ALTER TABLE `grants_proposal_review`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `procurement_bid`
--
ALTER TABLE `procurement_bid`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `procurement_tender`
--
ALTER TABLE `procurement_tender`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `procurement_tenderdocument`
--
ALTER TABLE `procurement_tenderdocument`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `procurement_tenderstatushistory`
--
ALTER TABLE `procurement_tenderstatushistory`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reporting_analytics_event`
--
ALTER TABLE `reporting_analytics_event`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `reporting_dashboard`
--
ALTER TABLE `reporting_dashboard`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reporting_dashboard_widget`
--
ALTER TABLE `reporting_dashboard_widget`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reporting_data_export`
--
ALTER TABLE `reporting_data_export`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `reporting_kpi`
--
ALTER TABLE `reporting_kpi`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `reporting_kpi_value`
--
ALTER TABLE `reporting_kpi_value`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `reporting_proposal_criterion`
--
ALTER TABLE `reporting_proposal_criterion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `reporting_proposal_criterion_response`
--
ALTER TABLE `reporting_proposal_criterion_response`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `reporting_reb_grant_budget`
--
ALTER TABLE `reporting_reb_grant_budget`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `reporting_report`
--
ALTER TABLE `reporting_report`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `reporting_report_schedule`
--
ALTER TABLE `reporting_report_schedule`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reporting_supplier_criterion`
--
ALTER TABLE `reporting_supplier_criterion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `reporting_supplier_criterion_response`
--
ALTER TABLE `reporting_supplier_criterion_response`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `training_assessment_result`
--
ALTER TABLE `training_assessment_result`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `training_course_module`
--
ALTER TABLE `training_course_module`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `training_module_progress`
--
ALTER TABLE `training_module_progress`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `training_training_assessment`
--
ALTER TABLE `training_training_assessment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `training_training_category`
--
ALTER TABLE `training_training_category`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `training_training_certificate`
--
ALTER TABLE `training_training_certificate`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `training_training_course`
--
ALTER TABLE `training_training_course`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `training_training_enrollment`
--
ALTER TABLE `training_training_enrollment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `training_training_session`
--
ALTER TABLE `training_training_session`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `training_training_session_facilitators`
--
ALTER TABLE `training_training_session_facilitators`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ai_engine_allocation_algorithm`
--
ALTER TABLE `ai_engine_allocation_algorithm`
  ADD CONSTRAINT `ai_engine_allocation_created_by_id_6e8d067f_fk_core_user` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `ai_engine_allocation_factor`
--
ALTER TABLE `ai_engine_allocation_factor`
  ADD CONSTRAINT `ai_engine_allocation_created_by_id_770dc5bd_fk_core_user` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `ai_engine_allocation_run`
--
ALTER TABLE `ai_engine_allocation_run`
  ADD CONSTRAINT `ai_engine_allocation_algorithm_id_d442ae39_fk_ai_engine` FOREIGN KEY (`algorithm_id`) REFERENCES `ai_engine_allocation_algorithm` (`id`),
  ADD CONSTRAINT `ai_engine_allocation_run_created_by_id_58e155bf_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `ai_engine_optimization_recommendation`
--
ALTER TABLE `ai_engine_optimization_recommendation`
  ADD CONSTRAINT `ai_engine_optimizati_created_by_id_6f67c7cc_fk_core_user` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `ai_engine_optimizati_implemented_by_id_090113e3_fk_core_user` FOREIGN KEY (`implemented_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `ai_engine_optimizati_proposal_id_7f74558d_fk_grants_gr` FOREIGN KEY (`proposal_id`) REFERENCES `grants_grant_proposal` (`id`),
  ADD CONSTRAINT `ai_engine_optimizati_school_id_0c03dc63_fk_core_scho` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`);

--
-- Constraints for table `ai_engine_proposalanomaly`
--
ALTER TABLE `ai_engine_proposalanomaly`
  ADD CONSTRAINT `ai_engine_proposalan_proposal_id_5b085c8d_fk_grants_gr` FOREIGN KEY (`proposal_id`) REFERENCES `grants_grant_proposal` (`id`);

--
-- Constraints for table `ai_engine_proposalprediction`
--
ALTER TABLE `ai_engine_proposalprediction`
  ADD CONSTRAINT `ai_engine_proposalpr_proposal_id_862b764d_fk_grants_gr` FOREIGN KEY (`proposal_id`) REFERENCES `grants_grant_proposal` (`id`);

--
-- Constraints for table `ai_engine_proposal_allocation_score`
--
ALTER TABLE `ai_engine_proposal_allocation_score`
  ADD CONSTRAINT `ai_engine_proposal_a_allocation_run_id_da90fcbc_fk_ai_engine` FOREIGN KEY (`allocation_run_id`) REFERENCES `ai_engine_allocation_run` (`id`),
  ADD CONSTRAINT `ai_engine_proposal_a_proposal_id_ca34296d_fk_grants_gr` FOREIGN KEY (`proposal_id`) REFERENCES `grants_grant_proposal` (`id`);

--
-- Constraints for table `ai_engine_recommendationaction`
--
ALTER TABLE `ai_engine_recommendationaction`
  ADD CONSTRAINT `ai_engine_recommendationaction_user_id_0fe752f7_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `ai_engine_risk_assessment`
--
ALTER TABLE `ai_engine_risk_assessment`
  ADD CONSTRAINT `ai_engine_risk_asses_proposal_id_c8c151f2_fk_grants_gr` FOREIGN KEY (`proposal_id`) REFERENCES `grants_grant_proposal` (`id`),
  ADD CONSTRAINT `ai_engine_risk_asses_resolved_by_id_29166d7f_fk_core_user` FOREIGN KEY (`resolved_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `ai_engine_risk_assessment_created_by_id_35bcb65d_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `ai_engine_risk_assessment_school_id_bcb72f81_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `budget_budget_line_item`
--
ALTER TABLE `budget_budget_line_item`
  ADD CONSTRAINT `budget_budget_line_i_budget_category_id_ad34c87c_fk_budget_bu` FOREIGN KEY (`budget_category_id`) REFERENCES `budget_budget_category` (`id`),
  ADD CONSTRAINT `budget_budget_line_i_related_proposal_id_ca9f7066_fk_grants_gr` FOREIGN KEY (`related_proposal_id`) REFERENCES `grants_grant_proposal` (`id`),
  ADD CONSTRAINT `budget_budget_line_i_school_budget_id_308b2f14_fk_budget_sc` FOREIGN KEY (`school_budget_id`) REFERENCES `budget_school_budget` (`id`),
  ADD CONSTRAINT `budget_budget_line_item_created_by_id_219277f8_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `budget_budget_period`
--
ALTER TABLE `budget_budget_period`
  ADD CONSTRAINT `budget_budget_period_created_by_id_f033cea1_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `budget_budget_report`
--
ALTER TABLE `budget_budget_report`
  ADD CONSTRAINT `budget_budget_report_generated_by_id_c40c9e4d_fk_core_user_id` FOREIGN KEY (`generated_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `budget_budget_report_school_budget_id_414a0405_fk_budget_sc` FOREIGN KEY (`school_budget_id`) REFERENCES `budget_school_budget` (`id`);

--
-- Constraints for table `budget_budget_transfer`
--
ALTER TABLE `budget_budget_transfer`
  ADD CONSTRAINT `budget_budget_transf_destination_line_ite_f471d759_fk_budget_bu` FOREIGN KEY (`destination_line_item_id`) REFERENCES `budget_budget_line_item` (`id`),
  ADD CONSTRAINT `budget_budget_transf_source_line_item_id_b13da18c_fk_budget_bu` FOREIGN KEY (`source_line_item_id`) REFERENCES `budget_budget_line_item` (`id`),
  ADD CONSTRAINT `budget_budget_transfer_approved_by_id_fbf3e0a0_fk_core_user_id` FOREIGN KEY (`approved_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `budget_budget_transfer_created_by_id_fae478e9_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `budget_expenditure`
--
ALTER TABLE `budget_expenditure`
  ADD CONSTRAINT `budget_expenditure_approved_by_id_3f0bb80f_fk_core_user_id` FOREIGN KEY (`approved_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `budget_expenditure_budget_line_item_id_9507dab3_fk_budget_bu` FOREIGN KEY (`budget_line_item_id`) REFERENCES `budget_budget_line_item` (`id`),
  ADD CONSTRAINT `budget_expenditure_created_by_id_09348f00_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `budget_school_budget`
--
ALTER TABLE `budget_school_budget`
  ADD CONSTRAINT `budget_school_budget_approved_by_id_70465744_fk_core_user_id` FOREIGN KEY (`approved_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `budget_school_budget_budget_period_id_d9dd972c_fk_budget_bu` FOREIGN KEY (`budget_period_id`) REFERENCES `budget_budget_period` (`id`),
  ADD CONSTRAINT `budget_school_budget_created_by_id_debe0a95_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `budget_school_budget_school_id_b14fecbe_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`);

--
-- Constraints for table `community_announcement`
--
ALTER TABLE `community_announcement`
  ADD CONSTRAINT `community_announcement_created_by_id_1908c9a7_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `community_announcement_target_schools`
--
ALTER TABLE `community_announcement_target_schools`
  ADD CONSTRAINT `community_announceme_announcement_id_0a828dfa_fk_community` FOREIGN KEY (`announcement_id`) REFERENCES `community_announcement` (`id`),
  ADD CONSTRAINT `community_announceme_school_id_206b4bae_fk_core_scho` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`);

--
-- Constraints for table `community_community_event`
--
ALTER TABLE `community_community_event`
  ADD CONSTRAINT `community_community__contact_person_id_ce0f9cae_fk_core_user` FOREIGN KEY (`contact_person_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `community_community_event_created_by_id_b20a807c_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `community_community_event_organizers`
--
ALTER TABLE `community_community_event_organizers`
  ADD CONSTRAINT `community_community__communityevent_id_b2fcd733_fk_community` FOREIGN KEY (`communityevent_id`) REFERENCES `community_community_event` (`id`),
  ADD CONSTRAINT `community_community__user_id_07019dfd_fk_core_user` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `community_community_event_target_schools`
--
ALTER TABLE `community_community_event_target_schools`
  ADD CONSTRAINT `community_community__communityevent_id_3e5c7794_fk_community` FOREIGN KEY (`communityevent_id`) REFERENCES `community_community_event` (`id`),
  ADD CONSTRAINT `community_community__school_id_c488aa0e_fk_core_scho` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`);

--
-- Constraints for table `community_community_forum`
--
ALTER TABLE `community_community_forum`
  ADD CONSTRAINT `community_community_forum_created_by_id_a7f09439_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `community_community_forum_school_id_3ccf3391_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`);

--
-- Constraints for table `community_community_forum_moderators`
--
ALTER TABLE `community_community_forum_moderators`
  ADD CONSTRAINT `community_community__communityforum_id_80b8a621_fk_community` FOREIGN KEY (`communityforum_id`) REFERENCES `community_community_forum` (`id`),
  ADD CONSTRAINT `community_community__user_id_1ed27362_fk_core_user` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `community_community_message`
--
ALTER TABLE `community_community_message`
  ADD CONSTRAINT `community_community__replied_to_id_6c587ec2_fk_community` FOREIGN KEY (`replied_to_id`) REFERENCES `community_community_message` (`id`),
  ADD CONSTRAINT `community_community_message_school_id_31ff80d5_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`),
  ADD CONSTRAINT `community_community_message_sender_id_96c39389_fk_core_user_id` FOREIGN KEY (`sender_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `community_community_message_recipients`
--
ALTER TABLE `community_community_message_recipients`
  ADD CONSTRAINT `community_community__communitymessage_id_d56bbee3_fk_community` FOREIGN KEY (`communitymessage_id`) REFERENCES `community_community_message` (`id`),
  ADD CONSTRAINT `community_community__user_id_973a2b4a_fk_core_user` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `community_feedback`
--
ALTER TABLE `community_feedback`
  ADD CONSTRAINT `community_feedback_resolved_by_id_974f2645_fk_core_user_id` FOREIGN KEY (`resolved_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `community_feedback_reviewed_by_id_292508a6_fk_core_user_id` FOREIGN KEY (`reviewed_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `community_feedback_school_id_c7d56c49_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`),
  ADD CONSTRAINT `community_feedback_submitted_by_id_4fa007ce_fk_core_user_id` FOREIGN KEY (`submitted_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `community_forum_post`
--
ALTER TABLE `community_forum_post`
  ADD CONSTRAINT `community_forum_post_created_by_id_b7767713_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `community_forum_post_edited_by_id_a5206ed4_fk_core_user_id` FOREIGN KEY (`edited_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `community_forum_post_parent_post_id_a0b6f13d_fk_community` FOREIGN KEY (`parent_post_id`) REFERENCES `community_forum_post` (`id`),
  ADD CONSTRAINT `community_forum_post_topic_id_dbaba187_fk_community` FOREIGN KEY (`topic_id`) REFERENCES `community_forum_topic` (`id`);

--
-- Constraints for table `community_forum_topic`
--
ALTER TABLE `community_forum_topic`
  ADD CONSTRAINT `community_forum_topi_forum_id_9e4d0d58_fk_community` FOREIGN KEY (`forum_id`) REFERENCES `community_community_forum` (`id`),
  ADD CONSTRAINT `community_forum_topic_created_by_id_3a5c9011_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `community_forum_topic_last_post_by_id_148f12d1_fk_core_user_id` FOREIGN KEY (`last_post_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `core_auditlog`
--
ALTER TABLE `core_auditlog`
  ADD CONSTRAINT `core_auditlog_user_id_3797aaab_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `core_school`
--
ALTER TABLE `core_school`
  ADD CONSTRAINT `core_school_created_by_id_0559e6ce_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `core_school_user`
--
ALTER TABLE `core_school_user`
  ADD CONSTRAINT `core_school_user_assigned_by_id_a9eb8cb8_fk_core_user_id` FOREIGN KEY (`assigned_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `core_school_user_school_id_df605e87_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`),
  ADD CONSTRAINT `core_school_user_user_id_c6dd35a3_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `core_system_configuration`
--
ALTER TABLE `core_system_configuration`
  ADD CONSTRAINT `core_system_configuration_created_by_id_102929e6_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `core_user_groups`
--
ALTER TABLE `core_user_groups`
  ADD CONSTRAINT `core_user_groups_group_id_fe8c697f_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `core_user_groups_user_id_70b4d9b8_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `core_user_user_permissions`
--
ALTER TABLE `core_user_user_permissions`
  ADD CONSTRAINT `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `core_user_user_permissions_user_id_085123d3_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `grants_fund_allocation`
--
ALTER TABLE `grants_fund_allocation`
  ADD CONSTRAINT `grants_fund_allocati_proposal_id_19011cef_fk_grants_gr` FOREIGN KEY (`proposal_id`) REFERENCES `grants_grant_proposal` (`id`),
  ADD CONSTRAINT `grants_fund_allocation_allocated_by_id_f839097f_fk_core_user_id` FOREIGN KEY (`allocated_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `grants_fund_allocation_disbursed_by_id_a8908e53_fk_core_user_id` FOREIGN KEY (`disbursed_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `grants_grant_category`
--
ALTER TABLE `grants_grant_category`
  ADD CONSTRAINT `grants_grant_category_created_by_id_aacee909_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `grants_grant_proposal`
--
ALTER TABLE `grants_grant_proposal`
  ADD CONSTRAINT `grants_grant_proposa_grant_category_id_4b5c7fe9_fk_grants_gr` FOREIGN KEY (`grant_category_id`) REFERENCES `grants_grant_category` (`id`),
  ADD CONSTRAINT `grants_grant_proposal_approved_by_id_009dfe80_fk_core_user_id` FOREIGN KEY (`approved_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `grants_grant_proposal_created_by_id_0b9769a3_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `grants_grant_proposal_school_id_bb24290d_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`);

--
-- Constraints for table `grants_proposal_budget`
--
ALTER TABLE `grants_proposal_budget`
  ADD CONSTRAINT `grants_proposal_budg_proposal_id_06dcccf4_fk_grants_gr` FOREIGN KEY (`proposal_id`) REFERENCES `grants_grant_proposal` (`id`),
  ADD CONSTRAINT `grants_proposal_budget_created_by_id_db742513_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `grants_proposal_document`
--
ALTER TABLE `grants_proposal_document`
  ADD CONSTRAINT `grants_proposal_docu_proposal_id_02c76dbe_fk_grants_gr` FOREIGN KEY (`proposal_id`) REFERENCES `grants_grant_proposal` (`id`),
  ADD CONSTRAINT `grants_proposal_document_uploaded_by_id_25303237_fk_core_user_id` FOREIGN KEY (`uploaded_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `grants_proposal_review`
--
ALTER TABLE `grants_proposal_review`
  ADD CONSTRAINT `grants_proposal_revi_proposal_id_ad8472a6_fk_grants_gr` FOREIGN KEY (`proposal_id`) REFERENCES `grants_grant_proposal` (`id`),
  ADD CONSTRAINT `grants_proposal_review_reviewer_id_50ac1cc8_fk_core_user_id` FOREIGN KEY (`reviewer_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `procurement_bid`
--
ALTER TABLE `procurement_bid`
  ADD CONSTRAINT `procurement_bid_supplier_id_2e696167_fk_core_user_id` FOREIGN KEY (`supplier_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `procurement_bid_tender_id_3b6ca2a1_fk_procurement_tender_id` FOREIGN KEY (`tender_id`) REFERENCES `procurement_tender` (`id`);

--
-- Constraints for table `procurement_tender`
--
ALTER TABLE `procurement_tender`
  ADD CONSTRAINT `procurement_tender_created_by_id_94b01d94_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `procurement_tender_school_id_7549296b_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`);

--
-- Constraints for table `procurement_tenderdocument`
--
ALTER TABLE `procurement_tenderdocument`
  ADD CONSTRAINT `procurement_tenderdo_tender_id_e8f4ef72_fk_procureme` FOREIGN KEY (`tender_id`) REFERENCES `procurement_tender` (`id`),
  ADD CONSTRAINT `procurement_tenderdo_uploaded_by_id_5d012aab_fk_core_user` FOREIGN KEY (`uploaded_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `procurement_tenderstatushistory`
--
ALTER TABLE `procurement_tenderstatushistory`
  ADD CONSTRAINT `procurement_tenderst_changed_by_id_22862556_fk_core_user` FOREIGN KEY (`changed_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `procurement_tenderst_tender_id_0a47d206_fk_procureme` FOREIGN KEY (`tender_id`) REFERENCES `procurement_tender` (`id`);

--
-- Constraints for table `reporting_analytics_event`
--
ALTER TABLE `reporting_analytics_event`
  ADD CONSTRAINT `reporting_analytics_event_user_id_c0f6380a_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `reporting_dashboard`
--
ALTER TABLE `reporting_dashboard`
  ADD CONSTRAINT `reporting_dashboard_school_id_63c95789_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`),
  ADD CONSTRAINT `reporting_dashboard_user_id_bbd9be8f_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `reporting_dashboard_widget`
--
ALTER TABLE `reporting_dashboard_widget`
  ADD CONSTRAINT `reporting_dashboard__dashboard_id_c2f6d402_fk_reporting` FOREIGN KEY (`dashboard_id`) REFERENCES `reporting_dashboard` (`id`);

--
-- Constraints for table `reporting_data_export`
--
ALTER TABLE `reporting_data_export`
  ADD CONSTRAINT `reporting_data_export_school_id_04c5cdd9_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`),
  ADD CONSTRAINT `reporting_data_export_user_id_c4372e22_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `reporting_kpi`
--
ALTER TABLE `reporting_kpi`
  ADD CONSTRAINT `reporting_kpi_created_by_id_a9ce979b_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `reporting_kpi_value`
--
ALTER TABLE `reporting_kpi_value`
  ADD CONSTRAINT `reporting_kpi_value_calculated_by_id_b25167d0_fk_core_user_id` FOREIGN KEY (`calculated_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `reporting_kpi_value_kpi_id_a7d7daf6_fk_reporting_kpi_id` FOREIGN KEY (`kpi_id`) REFERENCES `reporting_kpi` (`id`),
  ADD CONSTRAINT `reporting_kpi_value_school_id_10ba7d7e_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`);

--
-- Constraints for table `reporting_proposal_criterion_response`
--
ALTER TABLE `reporting_proposal_criterion_response`
  ADD CONSTRAINT `reporting_proposal_c_criterion_id_6ddfba61_fk_reporting` FOREIGN KEY (`criterion_id`) REFERENCES `reporting_proposal_criterion` (`id`),
  ADD CONSTRAINT `reporting_proposal_c_proposal_id_6171cfc8_fk_grants_gr` FOREIGN KEY (`proposal_id`) REFERENCES `grants_grant_proposal` (`id`);

--
-- Constraints for table `reporting_report`
--
ALTER TABLE `reporting_report`
  ADD CONSTRAINT `reporting_report_created_by_id_1c6d7e8d_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `reporting_report_school_id_96fae51e_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`);

--
-- Constraints for table `reporting_report_schedule`
--
ALTER TABLE `reporting_report_schedule`
  ADD CONSTRAINT `reporting_report_sch_report_id_32be7f8f_fk_reporting` FOREIGN KEY (`report_id`) REFERENCES `reporting_report` (`id`),
  ADD CONSTRAINT `reporting_report_schedule_created_by_id_7fc1a5db_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `reporting_supplier_criterion_response`
--
ALTER TABLE `reporting_supplier_criterion_response`
  ADD CONSTRAINT `reporting_supplier_c_criterion_id_a368d50d_fk_reporting` FOREIGN KEY (`criterion_id`) REFERENCES `reporting_supplier_criterion` (`id`),
  ADD CONSTRAINT `reporting_supplier_c_supplier_id_427891c3_fk_core_user` FOREIGN KEY (`supplier_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `training_assessment_result`
--
ALTER TABLE `training_assessment_result`
  ADD CONSTRAINT `training_assessment__assessment_id_1bd66fce_fk_training_` FOREIGN KEY (`assessment_id`) REFERENCES `training_training_assessment` (`id`),
  ADD CONSTRAINT `training_assessment__enrollment_id_ea114498_fk_training_` FOREIGN KEY (`enrollment_id`) REFERENCES `training_training_enrollment` (`id`);

--
-- Constraints for table `training_course_module`
--
ALTER TABLE `training_course_module`
  ADD CONSTRAINT `training_course_modu_course_id_9b41d422_fk_training_` FOREIGN KEY (`course_id`) REFERENCES `training_training_course` (`id`),
  ADD CONSTRAINT `training_course_module_created_by_id_398a5729_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `training_module_progress`
--
ALTER TABLE `training_module_progress`
  ADD CONSTRAINT `training_module_prog_enrollment_id_067bfe6a_fk_training_` FOREIGN KEY (`enrollment_id`) REFERENCES `training_training_enrollment` (`id`),
  ADD CONSTRAINT `training_module_prog_module_id_00e815d4_fk_training_` FOREIGN KEY (`module_id`) REFERENCES `training_course_module` (`id`);

--
-- Constraints for table `training_training_assessment`
--
ALTER TABLE `training_training_assessment`
  ADD CONSTRAINT `training_training_as_created_by_id_34515157_fk_core_user` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `training_training_as_module_id_8f262f53_fk_training_` FOREIGN KEY (`module_id`) REFERENCES `training_course_module` (`id`);

--
-- Constraints for table `training_training_category`
--
ALTER TABLE `training_training_category`
  ADD CONSTRAINT `training_training_ca_created_by_id_c8470dc7_fk_core_user` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `training_training_certificate`
--
ALTER TABLE `training_training_certificate`
  ADD CONSTRAINT `training_training_ce_created_by_id_5572d734_fk_core_user` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `training_training_ce_enrollment_id_8c0fd39e_fk_training_` FOREIGN KEY (`enrollment_id`) REFERENCES `training_training_enrollment` (`id`);

--
-- Constraints for table `training_training_course`
--
ALTER TABLE `training_training_course`
  ADD CONSTRAINT `training_training_co_category_id_edd02ba2_fk_training_` FOREIGN KEY (`category_id`) REFERENCES `training_training_category` (`id`),
  ADD CONSTRAINT `training_training_course_approved_by_id_1c66e147_fk_core_user_id` FOREIGN KEY (`approved_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `training_training_course_created_by_id_df87213f_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `training_training_enrollment`
--
ALTER TABLE `training_training_enrollment`
  ADD CONSTRAINT `training_training_en_course_id_3bebaa9a_fk_training_` FOREIGN KEY (`course_id`) REFERENCES `training_training_course` (`id`),
  ADD CONSTRAINT `training_training_en_session_id_cfc36558_fk_training_` FOREIGN KEY (`session_id`) REFERENCES `training_training_session` (`id`),
  ADD CONSTRAINT `training_training_enrollment_user_id_70f1057a_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `training_training_session`
--
ALTER TABLE `training_training_session`
  ADD CONSTRAINT `training_training_se_course_id_d253b600_fk_training_` FOREIGN KEY (`course_id`) REFERENCES `training_training_course` (`id`),
  ADD CONSTRAINT `training_training_session_created_by_id_4101952f_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Constraints for table `training_training_session_facilitators`
--
ALTER TABLE `training_training_session_facilitators`
  ADD CONSTRAINT `training_training_se_trainingsession_id_c14642bb_fk_training_` FOREIGN KEY (`trainingsession_id`) REFERENCES `training_training_session` (`id`),
  ADD CONSTRAINT `training_training_se_user_id_86bf2066_fk_core_user` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
