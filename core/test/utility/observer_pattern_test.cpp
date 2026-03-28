//This file is part of Bertini 2.
//
//observer_pattern_test.cpp is free software: you can redistribute it and/or modify
//it under the terms of the GNU General Public License as published by
//the Free Software Foundation, either version 3 of the License, or
//(at your option) any later version.
//
//observer_pattern_test.cpp is distributed in the hope that it will be useful,
//but WITHOUT ANY WARRANTY; without even the implied warranty of
//MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//GNU General Public License for more details.
//
//You should have received a copy of the GNU General Public License
//along with observer_pattern_test.cpp.  If not, see <http://www.gnu.org/licenses/>.
//
// Copyright(C) 2015 - 2021 by Bertini2 Development Team
//
// See <http://www.gnu.org/licenses/> for a copy of the license,
// as well as COPYING.  Bertini2 is provided with permitted
// additional terms in the b2/licenses/ directory.

/**
\file observer_pattern_test.cpp Unit testing for the bertini2 observer/observable pattern.
*/

#include <boost/test/unit_test.hpp>

#include "bertini2/detail/observable.hpp"
#include "bertini2/detail/observer.hpp"
#include "bertini2/detail/events.hpp"


namespace {

// A concrete observable for testing. Exposes NotifyObservers publicly.
class TestObservable : public bertini::Observable
{
public:
	void DoSomething()
	{
		bertini::Event<TestObservable> e(*this);
		NotifyObservers(e);
	}
};


// A concrete observer that counts how many times it has been notified.
class CountingObserver : public bertini::Observer<TestObservable>
{
public:
	int count = 0;

	void Observe(bertini::AnyEvent const& e) override
	{
		if (dynamic_cast<bertini::Event<TestObservable> const*>(&e))
			++count;
	}
};

} // anonymous namespace


BOOST_AUTO_TEST_SUITE(observer_pattern)

using namespace bertini;

BOOST_AUTO_TEST_CASE(attach_observer_to_observable)
{
	TestObservable subject;
	CountingObserver obs;

	// should not throw
	BOOST_CHECK_NO_THROW(subject.AddObserver(obs));
}


BOOST_AUTO_TEST_CASE(observer_receives_notification)
{
	TestObservable subject;
	CountingObserver obs;

	subject.AddObserver(obs);
	subject.DoSomething();

	BOOST_CHECK_EQUAL(obs.count, 1);
}


BOOST_AUTO_TEST_CASE(multiple_observers_receive_notifications)
{
	TestObservable subject;
	CountingObserver obs1;
	CountingObserver obs2;
	CountingObserver obs3;

	subject.AddObserver(obs1);
	subject.AddObserver(obs2);
	subject.AddObserver(obs3);

	subject.DoSomething();
	subject.DoSomething();

	BOOST_CHECK_EQUAL(obs1.count, 2);
	BOOST_CHECK_EQUAL(obs2.count, 2);
	BOOST_CHECK_EQUAL(obs3.count, 2);
}


BOOST_AUTO_TEST_CASE(remove_observer_stops_notifications)
{
	TestObservable subject;
	CountingObserver obs;

	subject.AddObserver(obs);
	subject.DoSomething();
	BOOST_CHECK_EQUAL(obs.count, 1);

	subject.RemoveObserver(obs);
	subject.DoSomething();
	BOOST_CHECK_EQUAL(obs.count, 1);  // should not have incremented
}


BOOST_AUTO_TEST_CASE(duplicate_add_does_not_double_notify)
{
	TestObservable subject;
	CountingObserver obs;

	subject.AddObserver(obs);
	subject.AddObserver(obs);  // duplicate add

	subject.DoSomething();
	BOOST_CHECK_EQUAL(obs.count, 1);  // should only be notified once
}


BOOST_AUTO_TEST_CASE(remove_nonexistent_observer_is_safe)
{
	TestObservable subject;
	CountingObserver obs;

	// removing an observer that was never added should not throw
	BOOST_CHECK_NO_THROW(subject.RemoveObserver(obs));
}

BOOST_AUTO_TEST_SUITE_END()
