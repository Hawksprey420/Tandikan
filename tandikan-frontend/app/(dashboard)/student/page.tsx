'use client';

import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Sidebar } from '@/components/layout/sidebar';

export default function StudentDashboard() {
  const studentData = {
    name: 'John Doe',
    studentId: '2025-00001',
    program: 'Bachelor of Science in Computer Science',
    yearLevel: 2,
    semester: '2nd Semester, AY 2024-2025',
    enrollmentStatus: 'approved',
    totalUnits: 21,
    gpa: 3.75
  };

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar role="student" />
      
      <div className="flex-1 p-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Student Dashboard</h1>
          <p className="text-gray-600 mt-1">Welcome back, {studentData.name}</p>
        </div>

        {/* Status Cards */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-gray-600">
                Enrollment Status
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold">
                  {studentData.enrollmentStatus === 'approved' ? 'Approved' : 'Pending'}
                </span>
                <Badge variant={studentData.enrollmentStatus === 'approved' ? 'success' : 'warning'}>
                  {studentData.enrollmentStatus}
                </Badge>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-gray-600">
                Total Units
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">{studentData.totalUnits}</p>
              <p className="text-xs text-gray-500 mt-1">Current semester</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-gray-600">
                GPA
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">{studentData.gpa}</p>
              <p className="text-xs text-gray-500 mt-1">Overall average</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-gray-600">
                Year Level
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">{studentData.yearLevel}</p>
              <p className="text-xs text-gray-500 mt-1">{studentData.program}</p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Grid */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Current Schedule */}
          <Card>
            <CardHeader>
              <CardTitle>Current Schedule</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="border-l-4 border-blue-500 pl-4 py-2">
                  <h4 className="font-semibold text-gray-900">Data Structures</h4>
                  <p className="text-sm text-gray-600">CS 201 - MWF 9:00-10:30 AM</p>
                  <p className="text-xs text-gray-500">Room 301 | Prof. Smith</p>
                </div>
                <div className="border-l-4 border-green-500 pl-4 py-2">
                  <h4 className="font-semibold text-gray-900">Discrete Mathematics</h4>
                  <p className="text-sm text-gray-600">MATH 203 - TTh 1:00-2:30 PM</p>
                  <p className="text-xs text-gray-500">Room 205 | Prof. Johnson</p>
                </div>
                <div className="border-l-4 border-amber-500 pl-4 py-2">
                  <h4 className="font-semibold text-gray-900">Web Development</h4>
                  <p className="text-sm text-gray-600">CS 205 - MWF 2:00-3:30 PM</p>
                  <p className="text-xs text-gray-500">Lab 102 | Prof. Williams</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Payment Summary */}
          <Card>
            <CardHeader>
              <CardTitle>Payment Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Tuition Fee</span>
                  <span className="font-semibold">₱25,000.00</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Laboratory Fee</span>
                  <span className="font-semibold">₱5,000.00</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Miscellaneous</span>
                  <span className="font-semibold">₱3,500.00</span>
                </div>
                <div className="border-t pt-4 flex justify-between items-center">
                  <span className="font-bold text-gray-900">Total Amount</span>
                  <span className="text-xl font-bold text-blue-600">₱33,500.00</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Amount Paid</span>
                  <span className="font-semibold text-green-600">₱15,000.00</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-gray-900">Balance</span>
                  <span className="text-lg font-bold text-red-600">₱18,500.00</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-4 gap-4">
              <button className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors">
                <div className="text-3xl mb-2">📝</div>
                <p className="font-semibold text-gray-900">Enroll Subjects</p>
              </button>
              <button className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-green-500 hover:bg-green-50 transition-colors">
                <div className="text-3xl mb-2">💳</div>
                <p className="font-semibold text-gray-900">Make Payment</p>
              </button>
              <button className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-purple-500 hover:bg-purple-50 transition-colors">
                <div className="text-3xl mb-2">📄</div>
                <p className="font-semibold text-gray-900">View Records</p>
              </button>
              <button className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-amber-500 hover:bg-amber-50 transition-colors">
                <div className="text-3xl mb-2">📧</div>
                <p className="font-semibold text-gray-900">Messages</p>
              </button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
