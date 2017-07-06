! This routine is used for the momentum calculation in rf_sol_tracking.py.
! Originally it was written in Python, but the fact that it is an iterative calculation
! (each step depends on the previous one) makes it hard to vectorise, as has been done for the
! other calculation steps. So this small section is written in Fortran and compiled using f2py.
! Hopefully it should be relatively easy to understand what's going on.
! For compilation instructions, see the compiling_momentum_calc.md file in the magnet-table folder.

subroutine calcMomentum(freq, phase, gamma_start, dz, gamma_tilde_dash, phase_offset, t, gamma_dash, gamma, beta, p)
  implicit none
  
  ! Constants
  real(8), parameter :: pi = 4.0 * atan(1.0)
  real(8), parameter :: c = 299792458.0

  ! Input parameters
  real(8), intent(in)  :: freq
  real(8), intent(in)  :: phase
  real(8), intent(in)  :: gamma_start
  real(8), intent(in)  :: dz
  ! gamma_tilde_dash is the phasor spatial derivative of gamma
  ! It is constant in a constant electric field, and is derived directly from the electric field.
  ! Clearly, in a time-dependent field we need to know the phase as well.
  ! We can import a number of different field maps, each of which has its own phase offset.
  ! This allows us to model a long linac with arbitrary phase offsets for each cell.
  real(8), intent(in)  :: gamma_tilde_dash(:, :)
  ! We need to define the phase offset for each cell too.
  real(8), intent(in)  :: phase_offset(:)

  ! Output parameters
  real(8), intent(out) :: t(size(gamma_tilde_dash,2))
  real(8), intent(out) :: gamma_dash(size(gamma_tilde_dash,2))
  real(8), intent(out) :: gamma(size(gamma_tilde_dash,2))
  real(8), intent(out) :: beta(size(gamma_tilde_dash,2))
  real(8), intent(out) :: p(size(gamma_tilde_dash,2))

  ! Variables
  real(8) :: omega
  real(8) :: dt
  integer i
  integer j

  ! Do the calculation of the initial step
  omega = 2 * pi * freq
  gamma(1) = gamma_start
  beta(1) = sqrt(1.0 - 1.0 / gamma(1) ** 2.0)
  p(1) = gamma(1) * beta(1)
  if (freq .eq. 0) then
    t(1) = 0
  else
    t(1) = phase / (360.0 * freq)
  end if

  do i = 1, size(gamma_tilde_dash,2) - 1
    ! Calculate the actual change in gamma (gamma_dash is defined as d(gamma)/dz)
	! This is the sum over all the RF sources, taking into account the phase offset of each one.
	do j = 1, size(gamma_tilde_dash,1)
      gamma_dash(i) = gamma_dash(i) + gamma_tilde_dash(j,i) * cos(omega * t(i) + phase_offset(j))
	end do
    gamma(i+1) = gamma(i) + gamma_dash(i) * dz
	! Calculate the momentum and beta
    p(i+1) = sqrt(gamma(i+1) ** 2.0 - 1.0)
    beta(i+1) = p(i+1) / gamma(i+1)
	! Calculate the time step - need to be careful when gamma_dash is zero
    if (gamma_dash(i) .eq. 0) then
      dt = 1 / (beta(i) * c)
    else
      dt = (p(i+1) - p(i)) / (gamma_dash(i) * c)
    end if
    t(i+1) = t(i) + dt
  end do
end subroutine
