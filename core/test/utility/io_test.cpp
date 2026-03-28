//This file is part of Bertini 2.
//
//io_test.cpp is free software: you can redistribute it and/or modify
//it under the terms of the GNU General Public License as published by
//the Free Software Foundation, either version 3 of the License, or
//(at your option) any later version.
//
//io_test.cpp is distributed in the hope that it will be useful,
//but WITHOUT ANY WARRANTY; without even the implied warranty of
//MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//GNU General Public License for more details.
//
//You should have received a copy of the GNU General Public License
//along with io_test.cpp.  If not, see <http://www.gnu.org/licenses/>.
//
// Copyright(C) 2015 - 2021 by Bertini2 Development Team
//
// See <http://www.gnu.org/licenses/> for a copy of the license,
// as well as COPYING.  Bertini2 is provided with permitted
// additional terms in the b2/licenses/ directory.

/**
\file io_test.cpp Unit testing for bertini2 file I/O utilities.
*/

#include <boost/test/unit_test.hpp>

#include "bertini2/io/file_utilities.hpp"

#include <fstream>
#include <filesystem>


BOOST_AUTO_TEST_SUITE(file_utilities)

using namespace bertini;

BOOST_AUTO_TEST_CASE(open_valid_file)
{
	// create a temporary file
	Path tmp = std::filesystem::temp_directory_path() / "b2_test_open_valid.txt";
	{
		std::ofstream out(tmp);
		out << "hello bertini2";
	}

	ifstream in;
	BOOST_CHECK_NO_THROW(OpenInFileThrowIfFail(in, tmp));
	BOOST_CHECK(in.is_open());

	in.close();
	std::filesystem::remove(tmp);
}


BOOST_AUTO_TEST_CASE(open_nonexistent_file_throws)
{
	Path nonexistent("/tmp/b2_test_this_file_does_not_exist_12345.txt");

	// make sure it really doesn't exist
	std::filesystem::remove(nonexistent);

	ifstream in;
	BOOST_CHECK_THROW(OpenInFileThrowIfFail(in, nonexistent), std::runtime_error);
}


BOOST_AUTO_TEST_CASE(open_directory_throws)
{
	Path dir = std::filesystem::temp_directory_path() / "b2_test_dir";
	std::filesystem::create_directories(dir);

	ifstream in;
	BOOST_CHECK_THROW(OpenInFileThrowIfFail(in, dir), std::runtime_error);

	std::filesystem::remove(dir);
}


BOOST_AUTO_TEST_CASE(file_to_string_reads_contents)
{
	Path tmp = std::filesystem::temp_directory_path() / "b2_test_file_to_string.txt";
	std::string expected_content = "line1\nline2\nline3";
	{
		std::ofstream out(tmp);
		out << expected_content;
	}

	std::string result = FileToString(tmp);
	BOOST_CHECK_EQUAL(result, expected_content);

	std::filesystem::remove(tmp);
}


BOOST_AUTO_TEST_CASE(file_to_string_nonexistent_throws)
{
	Path nonexistent("/tmp/b2_test_fts_nonexistent_67890.txt");
	std::filesystem::remove(nonexistent);

	BOOST_CHECK_THROW(FileToString(nonexistent), std::runtime_error);
}

BOOST_AUTO_TEST_SUITE_END()
